#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from requests import get
from requests import post
import json
import base64

class SpotifyAPIHandler:
    def __init__(self):
        load_dotenv()

        self.CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        self.AUTH_URL = "https://accounts.spotify.com/api/token"
        #Save the access token
        self.get_token()

        #Need to pass access token into header to send properly formed GET request to API server
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        self.BASE_URL = 'https://api.spotify.com/v1/'

    def get_token(self):
        auth_string = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes).decode('utf-8'))

        self.AUTH_URL = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        result = post(self.AUTH_URL, headers=headers, data=data)
        json_result = json.loads(result.content)
        self.access_token = json_result['access_token']

    def get_auth_header(self, token):
        return {
            'Authorization': f'Bearer {token}'
        }

    def search_for_artist(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header(self.access_token)
        query = f"?q={artist_name}&type=artist&limit=1"

        query_url = url + query
        print(query_url)
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)
        print(json_result)

    # def get_genres(self, artist_id):
    # #     CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    # #     CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
    # #     AUTH_URL = "https://accounts.spotify.com/api/token"
    # #     auth_response = requests.post(AUTH_URL, {
    # #     'grant_type': 'client_credentials',
    # #     'client_id': CLIENT_ID,
    # #     'client_secret': CLIENT_SECRET,
    # # })
    # #     #Convert response to JSON
    #     # auth_response_data = self.auth_response.json()

    #     # #Save the access token
    #     # self.access_token = auth_response_data['access_token']

    #     # #Need to pass access token into header to send properly formed GET request to API server
    #     # self.headers = {
    #     #     'Authorization': 'Bearer {token}'.format(token=self.access_token)
    #     # }
    #     # self.BASE_URL = 'https://api.spotify.com/v1/'


    #     try:
    #         response = requests.get(self.BASE_URL + 'artists/' + artist_id, headers=self.headers)
    #         data = response.json()

    #         if response.status_code == 200:
    #             if  0 == len(data['name']):
    #                 return data['name'] + " has no listed genres"
    #             else:
    #                 return f"The genres of {data['name']} are {' '.join(data['genres'])}"
    #         else:
    #             return f"Error: Unable to fetch weather data. Status code: {response.status_code}"

    #     except requests.RequestException as e:
    #         return f"Error: {str(e)}"

    # def get_profile(self):
    #     try:
    #         response = requests.get(self.BASE_URL + 'me', headers=self.headers)
    #         data = response.json()

    #         if response.status_code == 200:
    #             return f"User Profile: {data}"
    #         else:
    #             return f"Error: Unable to fetch user profile. Status code: {response.status_code}"

    #     except requests.RequestException as e:
    #         return f"Error: {str(e)}"
        
if __name__ == "__main__":
        spotify = SpotifyAPIHandler()
        spotify.search_for_artist("Ado")
        #print(SpotifyAPIHandler().get_genres(city))