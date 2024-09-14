import requests
import json
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time

def get_weather(city_name, api_key):
    # Base URL for OpenWeather current weather data
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        'q': city_name,        # City name
        'appid': api_key,      # API key
        'units': 'metric'      # Units for temperature (metric, imperial, or standard)
    }
    
    # Make the HTTP GET request to the OpenWeather API
    response = requests.get(base_url, params=params)
    
    # Print response status code and raw text for debugging
    print(f"Response Status Code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON data from the response
        data = response.json()
        
        # Extract relevant information from the response
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        # Create a dictionary with weather data for the city
        weather_data = {
            'city': city_name.capitalize(),
            'temperature': main['temp'],
            'humidity': main['humidity'],
            'condition': weather['description'].capitalize(),
            'wind_speed': wind['speed']
        }
        
        return weather_data
    else:
        # Return an error message if the request was unsuccessful
        print(f"Error: Could not retrieve weather for '{city_name}' (HTTP {response.status_code})")
        return None

def main():
    # Your OpenWeather API key
    api_key = "79d08796032858d8504f2f893c77115f"  # Replace with your valid API key
    
    # Get weather data for 3 cities
    cities = ["Ratnapura", "Nugegoda", "Negombo"]
    
    # Initialize an empty list to hold weather data for all cities
    weather_data_list = []
    
    for city in cities:
        city_weather = get_weather(city, api_key)
        if city_weather:
            weather_data_list.append(city_weather)
    
    # Store weather data directly
    weather_data_json = json.dumps(weather_data_list, indent=4)

    # MQTT client setup
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker\n")
        else:
            print(f"Connection failed with code {rc}")

    client = mqtt.Client(mqtt_client.CallbackAPIVersion.VERSION1, "PythonPub")
    client.on_connect = on_connect

    broker_address = "test.mosquitto.org"  # Broker's address
    broker_port = 1883
    keepalive = 60
    qos = 2
    publish_topic = "IOT_JSON"

    # Connect to the MQTT broker
    client.connect(broker_address, broker_port, keepalive)

    # Start the MQTT loop to handle network traffic
    client.loop_start()

    try:
        while True:
            # Publish the weather data directly
            client.publish(publish_topic, weather_data_json, qos=qos)
            print(f"Published message '{weather_data_json}' to topic '{publish_topic}'\n")
            
            # Wait for a moment to simulate some client activity
            time.sleep(6)

    except KeyboardInterrupt:
        # Disconnect from the MQTT broker
        pass

    client.loop_stop()
    client.disconnect()

    print("Disconnected from the MQTT broker")

if __name__ == "__main__":
    main()


