import openrouteservice
import json
import folium

# Initialize ORS client (Replace with your actual API key)
api_key = "203ab3ce3597851110001cf6248dc8129e533c54ea28bccad529abe"
client = openrouteservice.Client(key=api_key)

# Hardcoded start and end locations (Example: India Gate to Red Fort)
start = [77.2295, 28.6129]  # Longitude, Latitude (India Gate)
end = [77.2408, 28.6562]    # Longitude, Latitude (Red Fort)

# Fetch route from ORS
route = client.directions(
    coordinates=[start, end],
    profile='driving-car',
    format='geojson'
)

# Extract route coordinates
if "features" in route and len(route["features"]) > 0:
    coordinates = route["features"][0]["geometry"]["coordinates"]
else:
    raise KeyError("ORS response does not contain 'features'.")

# Save response for debugging
with open("ors_response.json", "w") as f:
    json.dump(route, f, indent=4)

print("Route successfully retrieved and saved!")

# **Visualization using Folium**
# Create a map centered at the start location
m = folium.Map(location=[start[1], start[0]], zoom_start=14)

# Add route polyline
folium.PolyLine([(lat, lon) for lon, lat in coordinates], color="blue", weight=5).add_to(m)

# Add markers for start and end points
folium.Marker([start[1], start[0]], popup="Start: India Gate", icon=folium.Icon(color="green")).add_to(m)
folium.Marker([end[1], end[0]], popup="End: Red Fort", icon=folium.Icon(color="red")).add_to(m)

# Save map to an HTML file
m.save("route_map.html")
print("Map saved as route_map.html. Open in a browser to view.")