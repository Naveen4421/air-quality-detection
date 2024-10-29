import requests
import gradio as gr

API_KEY = 'bfd62a913eee6486de309fef3a34a725'
BASE_URL = 'http://api.openweathermap.org/data/2.5/air_pollution?'

def get_coordinates(city):
    """Fetch coordinates for the specified city."""
    geocode_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(geocode_url)

    if response.status_code != 200:
        return f"Error fetching data for city '{city}': {response.json().get('message', 'Unknown error')}"
    
    data = response.json()
    return data['coord']['lat'], data['coord']['lon']

def get_air_quality(lat, lon):
    """Fetch air quality data using latitude and longitude."""
    air_quality_url = f"{BASE_URL}lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(air_quality_url)

    if response.status_code != 200:
        return "Error fetching air quality data: " + response.json().get('message', 'Unknown error')

    return response.json()

def assess_air_quality(aqi):
    """Determine if the air quality is bad based on AQI."""
    return aqi > 100

def display_air_quality(city):
    """Main function to display air quality."""
    coordinates = get_coordinates(city)
    
    if isinstance(coordinates, str):  # Check if an error message is returned
        return coordinates
    
    lat, lon = coordinates
    air_quality_data = get_air_quality(lat, lon)
    
    if isinstance(air_quality_data, str):  # Check for error messages
        return air_quality_data

    aqi = air_quality_data['list'][0]['main']['aqi']
    pollutants = air_quality_data['list'][0]['components']
    
    output = f"Air Quality Index (AQI) for {city}: {aqi}\n"
    output += "Pollutant concentrations (µg/m³):\n"
    
    for pollutant, value in pollutants.items():
        output += f"{pollutant}: {value}\n"

    if assess_air_quality(aqi):
        output += "\nWarning: The air quality is considered bad.\nRecommended actions:\n"
        output += "- Limit outdoor activities.\n"
        output += "- Use air purifiers indoors.\n"
        output += "- Wear masks if going outside.\n"
        output += "- Keep windows closed."
    else:
        output += "\nThe air quality is good. Keep the environment the same to maintain it!"
    
    return output

# Gradio Interface
iface = gr.Interface(fn=display_air_quality,
                     inputs="text",
                     outputs="text",
                     title="Air Quality Checker",
                     description="Enter a city name to check its air quality.")

if __name__ == '__main__':
    iface.launch()
