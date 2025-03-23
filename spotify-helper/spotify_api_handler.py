import os
import sys
import requests

class SpotifyAPIHandler:
    def __init__(self):
        self.CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        self.AUTH_URL = "https://accounts.spotify.com/api/token"
        self.auth_response = requests.post(self.AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': self.CLIENT_ID,
        'client_secret': self.CLIENT_SECRET,
        
    })
        auth_response_data = self.auth_response.json()

        #Save the access token
        self.access_token = auth_response_data['access_token']

        #Need to pass access token into header to send properly formed GET request to API server
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        self.BASE_URL = 'https://api.spotify.com/v1/'

    def get_genres(self, artist_id):
    #     CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    #     CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
    #     AUTH_URL = "https://accounts.spotify.com/api/token"
    #     auth_response = requests.post(AUTH_URL, {
    #     'grant_type': 'client_credentials',
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET,
    # })
    #     #Convert response to JSON
        # auth_response_data = self.auth_response.json()

        # #Save the access token
        # self.access_token = auth_response_data['access_token']

        # #Need to pass access token into header to send properly formed GET request to API server
        # self.headers = {
        #     'Authorization': 'Bearer {token}'.format(token=self.access_token)
        # }
        # self.BASE_URL = 'https://api.spotify.com/v1/'


        try:
            response = requests.get(self.BASE_URL + 'artists/' + artist_id, headers=self.headers)
            data = response.json()

            if response.status_code == 200:
                if  0 == len(data['name']):
                    return data['name'] + " has no listed genres"
                else:
                    return f"The genres of {data['name']} are {" ".join(data['genres'])}"
            else:
                return f"Error: Unable to fetch weather data. Status code: {response.status_code}"

        except requests.RequestException as e:
            return f"Error: {str(e)}"

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            city = sys.argv[1]
            print(get_genres(city))
        else:
            print("Please provide a spotify artist id as an argument.")
