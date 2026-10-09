import os
import requests

from dotenv import load_dotenv
from geocoding_api import get_coordinates


load_dotenv()


def get_route_information(
    starting_location,
    destination,
    destination_state=None
):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_MAPS_API_KEY is missing from the .env file."
        )

    if not starting_location.strip():
        raise ValueError(
            "Starting location cannot be empty."
        )

    if not destination.strip():
        raise ValueError(
            "Destination cannot be empty."
        )

    start_coordinates = get_coordinates(
        starting_location,
        None
    )

    destination_coordinates = get_coordinates(
        destination,
        destination_state
    )

    start_latitude = start_coordinates["latitude"]
    start_longitude = start_coordinates["longitude"]

    destination_latitude = destination_coordinates["latitude"]
    destination_longitude = destination_coordinates["longitude"]

    url = (
        "https://routes.googleapis.com/"
        "directions/v2:computeRoutes"
    )

    request_body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": start_latitude,
                    "longitude": start_longitude
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_latitude,
                    "longitude": destination_longitude
                }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_UNAWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "METRIC"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "routes.distanceMeters,"
            "routes.duration,"
            "routes.legs"
        )
    }

    try:
        response = requests.post(
            url,
            json=request_body,
            headers=headers,
            timeout=20
        )

        if response.status_code == 401:
            raise ConnectionError(
                "Google Maps API key was rejected."
            )

        if response.status_code == 403:
            raise PermissionError(
                "Google Maps API access is not enabled "
                "or billing is not configured."
            )

        response.raise_for_status()

        data = response.json()

        if not data.get("routes"):
            raise ValueError(
                "No route was found between the locations."
            )

        route = data["routes"][0]

        distance_meters = route["distanceMeters"]

        duration_text = route["duration"]
        duration_seconds = float(
            duration_text.rstrip("s")
        )

        return {
            "starting_location": starting_location,
            "destination": destination,
            "distance_km": round(
                distance_meters / 1000,
                2
            ),
            "duration_hours": round(
                duration_seconds / 3600,
                2
            ),
            "duration_minutes": round(
                duration_seconds / 60
            ),
            "provider": "Google Maps Routes API",
            "route_type": "Driving"
        }

    except requests.exceptions.Timeout:
        raise ConnectionError(
            "Google Maps routing request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise ConnectionError(
            f"Google Maps routing request failed: {error}"
        )


if __name__ == "__main__":
    route = get_route_information(
        "Chandigarh",
        "Manali",
        "Himachal Pradesh"
    )

    print(route)