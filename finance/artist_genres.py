import os
import sys
import requests

def get_genres(artist_id):
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
      
    AUTH_URL = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
#     #Convert response to JSON
    auth_response_data = auth_response.json()

    #Save the access token
    access_token = auth_response_data['access_token']

    #Need to pass access token into header to send properly formed GET request to API server
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    BASE_URL = 'https://api.spotify.com/v1/'


    try:
        response = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)
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
