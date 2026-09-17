import os

import requests
from dotenv import load_dotenv


load_dotenv()


def is_shopping_place(place):

    name = place["name"].lower()
    address = (place["address"] or "").lower()

    shopping_keywords = [
        "shop",
        "store",
        "market",
        "mall",
        "shawl",
        "clothing",
        "handmade",
        "craft",
        "souvenir",
        "jewellery",
        "jewelry",
        "boutique"
    ]

    searchable_text = f"{name} {address}"

    return any(
        keyword in searchable_text
        for keyword in shopping_keywords
    )


def get_shopping_places(latitude, longitude):

    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise ValueError(
            "GEOAPIFY_API_KEY is missing from the .env file."
        )

    response = requests.get(
        "https://api.geoapify.com/v2/places",
        params={
            "categories": "commercial",
            "filter": f"circle:{longitude},{latitude},5000",
            "bias": f"proximity:{longitude},{latitude}",
            "limit": 20,
            "apiKey": api_key
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    shopping_places = []

    for feature in data.get("features", []):

        properties = feature.get("properties", {})

        name = properties.get("name")

        if not name:
            continue

        shopping_place = {
            "name": name,
            "address": properties.get("formatted"),
            "distance": properties.get("distance"),
            "category": "Shopping"
        }

        if is_shopping_place(shopping_place):
            shopping_places.append(shopping_place)

    return shopping_places


if __name__ == "__main__":

    try:

        shopping_places = get_shopping_places(
            32.2574,
            77.17481
        )

        print("\n===== SHOPPING PLACES =====")

        for place in shopping_places:

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