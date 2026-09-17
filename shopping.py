import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_shopping_places(latitude, longitude):

    api_key = os.getenv("GEOAPIFY_API_KEY")

    if not api_key:
        raise ValueError(
            "GEOAPIFY_API_KEY is missing from the .env file."
        )

    response = requests.get(
        "https://api.geoapify.com/v2/places",
        params={
            "categories": (
                "commercial.shopping_mall,"
                "commercial.marketplace,"
                "commercial.department_store,"
                "commercial.clothing,"
                "commercial.gift_and_souvenir"
            ),
            "filter": (
                f"circle:{longitude},{latitude},15000"
            ),
            "bias": (
                f"proximity:{longitude},{latitude}"
            ),
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
            f"Invalid shopping request: {response.text}"
        )

    response.raise_for_status()

    data = response.json()
    shopping_places = []

    irrelevant_keywords = [
        "regus",
        "office",
        "tower",
        "building",
        "kendra",
        "exchange money",
        "currency exchange",
        "exchange",
        "money",
        "час",
        "часы",
        "stationary",
        "parking",
        "warehouse",
        "factory",
        "vegetable",
        "fruit",
        "sabji",
        "farmers market",
        "monday market",
        "thursday market",
        "friday market",
        "entry"
    ]

    useful_keywords = [
        "mall",
        "market",
        "bazaar",
        "bazar",
        "shopping",
        "handloom",
        "handicraft",
        "textile",
        "clothing",
        "sari",
        "souvenir",
        "jewellery",
        "jewelry",
        "department store",
        "emporium",
        "craft"
    ]

    for feature in data.get("features", []):

        properties = feature.get("properties", {})

        name = properties.get("name")
        address = properties.get("formatted", "")

        if not name:
            continue

        categories = properties.get("categories", [])

        if isinstance(categories, list):
            category_text = " ".join(categories).lower()
        else:
            category_text = str(categories).lower()

        searchable_text = (
            f"{name} {address} {category_text}"
        ).lower()

        # Remove clearly irrelevant results
        if any(
            keyword in searchable_text
            for keyword in irrelevant_keywords
        ):
            continue

        # Keep only useful shopping-related results
        if not any(
            keyword in searchable_text
            for keyword in useful_keywords
        ):
            continue

        shopping_places.append({
            "name": name,
            "address": address or "Address unavailable",
            "distance": properties.get("distance", 0),
            "category": categories or "Shopping"
        })

    return shopping_places


if __name__ == "__main__":

    try:
        shopping_places = get_shopping_places(
            26.91962,
            75.78781
        )

        print("\n===== SHOPPING PLACES =====")

        if not shopping_places:
            print("No shopping places found.")

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