import openrouteservice
import json

# Initialize the ORS client5b3ce3597851110001cf6248dc8129e533c54ea28bccad529ab203ae
api_key = "5203ab3ce3597851110001cf6248dc8129e533c54ea28bccad529abe"
client = openrouteservice.Client(key=api_key)

# Define start and end coordinates
start = [8.681495, 49.41461]  # Example coordinates
end = [8.687872, 49.420318]

# Make the API request
route = client.directions(
    coordinates=[start, end],
    profile='driving-car',
    format='geojson'
)

# Check response structure and extract geometry
if "features" in route and len(route["features"]) > 0:
    coordinates = route["features"][0]["geometry"]["coordinates"]
    print("Route coordinates:", coordinates)
else:
    raise KeyError("ORS response does not contain 'features'.")

# Save response to JSON for debugging
with open("ors_response.json", "w") as f:
    json.dump(route, f, indent=4)

print("Route successfully retrieved and saved!")