import os
import requests

from dotenv import load_dotenv
from geocoding_api import get_coordinates

load_dotenv()

def get_route_information(
        starting_location,
        destination
):

    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise ValueError(
            "GEOAPIFY_API_KEY is missing from the .env file."
        )

    start_coordinates = get_coordinates(starting_location)
    destination_coordinates = get_coordinates(
                                destination,
                                state="Himachal Pradesh"
                                )

    start_latitude = start_coordinates["latitude"]
    start_longitude = start_coordinates["longitude"]

    destination_latitude = destination_coordinates["latitude"]
    destination_longitude = destination_coordinates["longitude"]

    waypoints = (
        f"{start_latitude},{start_longitude}|"
        f"{destination_latitude},{destination_longitude}"
    )

    response = requests.get(
        "https://api.geoapify.com/v1/routing",
        params={
            "waypoints": waypoints,
            "mode": "drive",
            "apiKey": api_key
        },
        timeout=20
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 401:
        raise ConnectionError(
            "Geoapify rejected the API key. "
            "Check the key and Routing API access."
        )

    response.raise_for_status()

    data = response.json()

    route_properties = data["features"][0]["properties"]

    distance_meters = route_properties["distance"]
    duration_seconds = route_properties["time"]

    return {    
    "starting_location": starting_location,
    "destination": destination,
    "distance_km": round(distance_meters / 1000, 2),
    "duration_hours": round(duration_seconds / 3600, 2),
    "duration_minutes": round(duration_seconds / 60)
}

if __name__ == "__main__":
    route = get_route_information("Chandigarh", "Manali")
    print(route)