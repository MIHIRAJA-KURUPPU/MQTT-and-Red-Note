import requests
import json

write_file_name = "openweathermap_data.json"

def get_weather(city_name, api_key):
    # Base URL for OpenWeather current weather data
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        'q': city_name,        # City name
        'appid': api_key,       # API key
        'units': 'metric'       # Units for temperature (metric, imperial, or standard)
    }
    
    # Make the HTTP GET request to the OpenWeather API
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON data from the response
        data = response.json()
        
        # Write the JSON data to a file
        with open(write_file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # The 'indent' parameter adds pretty formatting
        
        print("Data has been written to", write_file_name)
        
        # Extract relevant information from the response
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        # Print weather information
        print(f"Weather in {city_name.capitalize()}:")
        print(f"Temperature: {main['temp']}°C")
        print(f"Humidity: {main['humidity']}%")
        print(f"Condition: {weather['description'].capitalize()}")
        print(f"Wind Speed: {wind['speed']} m/s")
    else:
        # Print error message if request was unsuccessful
        print(f"Error: Could not retrieve weather for '{city_name}' (HTTP {response.status_code})")
        print(f"Response Text: {response.text}")

if __name__ == "__main__":
    # Your OpenWeather API key
    api_key = "17c3824f1382e7309370c91d8173294c"  # Replace with your valid API key
    
    # Get city name from user
    city_name = input("Enter the name of the city: ")
    
    # Fetch and display weather information
    get_weather(city_name, api_key)
