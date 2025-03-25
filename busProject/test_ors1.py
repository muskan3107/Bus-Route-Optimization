import openrouteservice
import requests
import json
import folium

# ORS API Key
ORS_API_KEY = "5203ab3ce3597851110001cf6248dc8129e533c54ea28bccad529abe"
client = openrouteservice.Client(key=ORS_API_KEY)

# Function to get coordinates from OpenStreetMap Nominatim API
def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if data:
        lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
        return [lon, lat]  # ORS uses [longitude, latitude]
    else:
        raise ValueError(f"Error: Could not find coordinates for {place_name}")

# Get user input for locations
start_location = input("Enter starting location: ")
end_location = input("Enter destination: ")

try:
    start_coords = get_coordinates(start_location)
    end_coords = get_coordinates(end_location)
    print(f"Start Coordinates: {start_coords}")
    print(f"End Coordinates: {end_coords}")

    # Fetch route from ORS
    route = client.directions(
        coordinates=[start_coords, end_coords],
        profile='driving-car',
        format='geojson'
    )

    # Extract coordinates from the response
    if "features" in route and route["features"]:
        route_coords = route["features"][0]["geometry"]["coordinates"]

        # Save route response for debugging
        with open("ors_route.json", "w") as f:
            json.dump(route, f, indent=4)

        # Create map centered at start location
        m = folium.Map(location=[start_coords[1], start_coords[0]], zoom_start=12)

        # Add route to the map
        folium.PolyLine([(lat, lon) for lon, lat in route_coords], color="blue", weight=5).add_to(m)

        # Add markers for start and end locations
        folium.Marker([start_coords[1], start_coords[0]], popup="Start", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([end_coords[1], end_coords[0]], popup="Destination", icon=folium.Icon(color="red")).add_to(m)

        # Save the map to an HTML file and display it
        map_filename = "route_map.html"
        m.save(map_filename)
        print(f"Route map saved as {map_filename}. Open this file in a browser to view the route.")

    else:
        print("Error: ORS response does not contain route data.")

except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")