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

    try:
        response = requests.get(
            "https://api.geoapify.com/v2/places",
            params={
                "categories": "tourism",
                "filter": f"circle:{longitude},{latitude},5000",
                "bias": f"proximity:{longitude},{latitude}",
                "limit": 20,
                "apiKey": api_key
            },
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        print("Unable to fetch sightseeing places.")
        print("Error:", error)
        return []

    places = []

    for feature in data.get("features", []):

        properties = feature.get("properties", {})

        name = properties.get("name")

        if not name:
            continue

        place = {
            "name": name,
            "address": properties.get("formatted"),
            "latitude": properties.get("lat"),
            "longitude": properties.get("lon"),
            "distance": properties.get("distance"),
            "category": properties.get("category")
        }

        places.append(place)

    return places


if __name__ == "__main__":

    try:

        places = get_places(
            32.2574,
            77.17481
        )

        print("\n===== PLACES TO VISIT =====")

        for place in places:

            print(f"\nName     : {place['name']}")
            print(f"Address  : {place['address']}")
            print(f"Distance : {place['distance']} metres")
            print(f"Category : {place['category']}")

    except requests.exceptions.RequestException as error:

        print("Geoapify request failed.")
        print(error)

    except ValueError as error:

        print("Configuration error.")
        print(error)