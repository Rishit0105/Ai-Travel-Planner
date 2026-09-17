import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_places(latitude, longitude):

    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise ValueError(
            "GEOAPIFY_API_KEY is missing from the .env file."
        )

    response = requests.get(
        "https://api.geoapify.com/v2/places",
        params={
            "categories": "tourism.sights",
            "filter": f"circle:{longitude},{latitude},15000",
            "bias": f"proximity:{longitude},{latitude}",
            "limit": 50,
            "apiKey": api_key
        },
        timeout=20
    )

    if response.status_code == 401:
        raise ConnectionError(
            "Geoapify rejected the API key. Check your API key."
        )

    if response.status_code == 400:
        raise ValueError(
            f"Invalid Geoapify places request: {response.text}"
        )

    response.raise_for_status()

    data = response.json()
    features = data.get("features", [])

    places = []

    for feature in features:

        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        coordinates = geometry.get("coordinates", [])

        if len(coordinates) < 2:
            continue

        places.append({
            "name": properties.get(
                "name",
                "Unnamed place"
            ),

            "address": properties.get(
                "formatted",
                "Address unavailable"
            ),

            "latitude": coordinates[1],
            "longitude": coordinates[0],

            "distance": properties.get(
                "distance",
                0
            ),

            "category": properties.get(
                "categories",
                ""
            )
        })

    return places