import os
import sys
import requests

def get_weather(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        return "Error: OpenWeatherMap API key not found in environment variables."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The weather in {city} is {description} with a temperature of {temp}°C."
        else:
            return f"Error: Unable to fetch weather data. Status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        print(get_weather(city))
    else:
        print("Please provide a city name as an argument.")
