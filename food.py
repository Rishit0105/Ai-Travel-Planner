import os

import requests
from dotenv import load_dotenv


load_dotenv()

def get_food_category(categories):

    for category in categories:

        if category == "catering.restaurant.indian":
            return "Indian Restaurant"

        if category ==  "catering.restaurant.international":
            return "International Restaurant"

        if category == "catering.restaurant":
            return "Restaurant"

        if category == "category.cafe":
            return "Cafe"

    return "Food Place"

def get_food_places(latitude, longitude):

    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise ValueError(
            "GEOAPIFY_API_KEY is missing from the .env file."
        )

    try:
        response = requests.get(
            "https://api.geoapify.com/v2/places",
            params={
                "categories": "catering.restaurant,catering.cafe",
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
        print("Unable to fetch food places.")
        print("Error:", error)
        return []

    food_places = []

    for feature in data.get("features", []):

        properties = feature.get("properties", {})

        name = properties.get("name")

        if not name:
            continue

        food_place = {
            "name": name,
            "address": properties.get("formatted"),
            "distance": properties.get("distance"),
            "category": get_food_category(
                properties.get("categories", [])
            )
        }

        food_places.append(food_place)

    return food_places


if __name__ == "__main__":

    try:

        food_places = get_food_places(
            32.2574,
            77.17481
        )

        print("\n===== FOOD PLACES =====")

        for place in food_places:

            print(f"\nName     : {place['name']}")
            print(f"Address  : {place['address']}")
            print(f"Distance : {place['distance']} metres")

    except requests.exceptions.RequestException as error:

        print("Geoapify request failed.")
        print(error)

    except ValueError as error:

        print("Configuration error.")
        print(error)