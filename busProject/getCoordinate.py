import requests
import time

def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    
    try:
        response = requests.get(url)
        
        # Check if the response is empty
        if response.status_code != 200 or not response.text.strip():
            raise ValueError(f"Error: Nominatim API returned an empty response for '{place_name}'.")

        # Parse the JSON response safely
        data = response.json()
        
        if data:
            lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
            return [lon, lat]  # ORS requires [longitude, latitude]
        else:
            raise ValueError(f"Error: No location found for '{place_name}'. Check the spelling.")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error: {e}")

# Adding a delay to prevent rate limits
time.sleep(1)