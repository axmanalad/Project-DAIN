import { z } from "zod";
import { exec } from "child_process";
import { promisify } from "util";
import axios from "axios";
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
            genres: z.string().describe("Genres of the artist"),
        })
        .describe("Genre information"),
    pricing: { pricePerUse: 0, currency: "USD" },
    handler: async ({ artist }, agentInfo, context) => {
      console.log(
        `User / Agent ${agentInfo.id} requested genres from ${artist})`
      );
        try {
          console.log(`User / Agent ${agentInfo.id} requested genres at ${artist}`);
          console.log("Test");
          const { stdout, stderr } = await execAsync(`python3 apis/get_genres.py "${artist}"`);
          // const apiResponse = await axios.get(
          //   `https://api.spotify.com/v1/search?q=${artist}&type=artist&limit=1`,
          //   {
          //     headers: {
          //       Authorization: `Bearer ${process.env.SPOTIFY_ACCESS_TOKEN}`, // Use the access token
          //       "Content-Type": "application/json",
          //     },
          //   }
          // );

          // const { genres } = apiResponse.data.artists.items[0];

          if (stderr) {
              throw new Error(stderr);
          }

          const genres = stdout.trim();
          if (!genres) {
              throw new Error("No genres found for the artist.");
          }

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
                data: { genres: "Error: Unable to fetch spotify data." + error },
                ui: new CardUIBuilder()
                    .title("Error")
                    .content("Unable to fetch spotify data.")
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
        scopes: [
          "user-read-private", 
          "user-read-email", 
          "playlist-read-private", // Example: Access private playlists
          "user-library-read",    // Example: Access user's saved tracks and albums
          "user-top-read"         // Example: Access user's top artists and tracks],
        ],
            onSuccess: async (agentId, tokens) => {
                tokenStore.set(agentId, tokens);
                console.log(`Tokens stored for agent: ${agentId}`);
          // Store tokens securely
        }
      }
    }
  },
    tools: [createOAuth2Tool("spotify"), getArtistGenres],
});

dainService.startNode().then(({ address }) => {
  console.log("DAIN Service is running at :" + address().port);
});
