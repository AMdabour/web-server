from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

IPAPI_URL = "http://ipapi.co/{}/json/"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
WEATHER_API_KEY = "08e357799f9a4a9d85f34153240207"  # Replace with your WeatherAPI API key

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/hello', methods=['GET'])
def hello():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # # Use a mock IP address for local testing
    # if client_ip == '127.0.0.1':
    #     client_ip = '8.8.8.8'  # Google's public DNS server IP
    
    visitor_name = request.args.get('visitor_name', 'Guest')

    # Fetch location data based on IP
    try:
        location_response = requests.get(IPAPI_URL.format(client_ip))
        location_response.raise_for_status()  # Raise an HTTPError for bad responses
        location_data = location_response.json()
        city = location_data.get("city", "Unknown")
        logging.debug(f"Location data: {location_data}")
    except requests.RequestException as e:
        logging.error(f"Error fetching location data: {e}")
        city = "Unknown"

    # Fetch weather data based on city from WeatherAPI
    try:
        if city != "Unknown":
            weather_response = requests.get(WEATHER_API_URL, params={
                'key': WEATHER_API_KEY,
                'q': city
            })
            weather_response.raise_for_status()  # Raise an HTTPError for bad responses
            weather_data = weather_response.json()
            logging.debug(f"weather data: {weather_data}")
            temperature = weather_data.get("current", {}).get("temp_c", "Unknown")
        else:
            temperature = "Unknown"
    except requests.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        temperature = "Unknown"

    response = {
        'client_ip': client_ip,
        'location': f"{city}",
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
