import { z } from "zod";
import { exec } from "child_process";
import { promisify } from "util";
import {
  defineDAINService,
  ToolConfig,
} from "@dainprotocol/service-sdk";
import { CardUIBuilder } from "@dainprotocol/utils";
import { OAuth2Tokens } from "@dainprotocol/service-sdk";

import { createOAuth2Tool } from "@dainprotocol/service-sdk";
import dotenv from 'dotenv';

dotenv.config(); // Load environment variables

const execAsync = promisify(exec);


const getArtistGenres: ToolConfig = {
    id: "get-genres",
    name: "Get Artist Genres",
    description: "Fetches listed genres of an artist",
    input: z
        .object({
            artist: z.string().describe("Artist spotify id"),
        })
        .describe("Input parameters for the spotify request"),
    output: z
        .object({
            genres: z.string().describe("Genre information"),
        })
        .describe("Genre information"),
    pricing: { pricePerUse: 0, currency: "USD" },
    handler: async ({ artist }, agentInfo, context) => {
        try {
            const { stdout, stderr } = await execAsync(`python artist_genres.py "${artist}"`);

            if (stderr) {
                throw new Error(stderr);
            }

            const genres = stdout.trim();

            return {
                text: genres,
                data: { genres },
                ui: new CardUIBuilder()
                    .title(`Artist genres`)
                    .content(genres)
                    .build(),
            };
        } catch (error) {
            console.error("Error executing Python script:", error);
            return {
                text: "An error occurred while fetching the info.",
                data: { genres: "Error: Unable to fetch spotify data." },
                ui: new CardUIBuilder()
                    .title("Error")
                    .content("Unable to fetch spotify data.")
                    .build(),
            };
        }
    },
};

const getWeatherConfig: ToolConfig = {
  id: "get-weather",
  name: "Get Weather",
  description: "Fetches current weather for a city",
  input: z
    .object({
      city: z.string().describe("City name"),
    })
    .describe("Input parameters for the weather request"),
  output: z
    .object({
      weather: z.string().describe("Weather information"),
    })
    .describe("Weather information"),
  pricing: { pricePerUse: 0, currency: "USD" },
  handler: async ({ city }, agentInfo, context) => {
    try {
      const { stdout, stderr } = await execAsync(`python weather_lookup.py "${city}"`);
      
      if (stderr) {
        throw new Error(stderr);
      }

      const weather = stdout.trim();

      return {
        text: weather,
        data: { weather },
        ui: new CardUIBuilder()
          .title(`Weather in ${city}`)
          .content(weather)
          .build(),
      };
    } catch (error) {
      console.error("Error executing Python script:", error);
      return {
        text: "An error occurred while fetching the weather.",
        data: { weather: "Error: Unable to fetch weather data." },
        ui: new CardUIBuilder()
          .title("Error")
          .content("Unable to fetch weather data.")
          .build(),
      };
    }
  },
};

const tokenStore = new Map<string, OAuth2Tokens>();

const dainService = defineDAINService({
  metadata: {
    title: "Spotify DAIN Service",
    description: "A DAIN service for getting info on things related to Spotify with Spotify API",
    version: "1.0.0",
    author: "Your Name",
    tags: ["artists", "music", "dain"],
    },

  identity: {
    apiKey: process.env.DAIN_API_KEY,
    },
    oauth2: {
    baseUrl: process.env.TUNNEL_URL, // Use the TUNNEL_URL from .env
    providers: {
      spotify: {
        clientId: process.env.SPOTIFY_CLIENT_ID,
        clientSecret: process.env.SPOTIFY_CLIENT_SECRET,
        authorizationUrl: "https://accounts.spotify.com/authorize",
        tokenUrl: "https://accounts.spotify.com/api/token",
        scopes: ["user-read-private", "user-read-email"],
            onSuccess: async (agentId, tokens) => {
                tokenStore.set(agentId, tokens);
                console.log(`Tokens stored for agent: ${agentId}`);
          // Store tokens securely
        }
      }
    }
  },
    tools: [createOAuth2Tool("spotify"),getWeatherConfig, getArtistGenres],
});

dainService.startNode().then(({ address }) => {
  console.log("DAIN Service is running at :" + address().port);
});
