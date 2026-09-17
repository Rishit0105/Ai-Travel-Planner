import requests


def get_coordinates(destination, state=None):

    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": destination,
                "count": 5,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        response.raise_for_status()

    except requests.exceptions.RequestException:
        raise ConnectionError(
            "Unable to connect to the geocoding service."
        )

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(
            f"Could not find destination: {destination}"
        )

    result = None

    for place in data["results"]:

        if state is None or place.get("admin1") == state:
            result = place
            break

    if result is None:
        raise ValueError(
            f"Could not find {destination} in {state}."
        )

    return {
        "name": result["name"],
        "state": result.get("admin1"),
        "country": result.get("country"),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


# Test code: runs only when this file is executed directly
if __name__ == "__main__":

    coordinates = get_coordinates(
        "Manali",
        "Himachal Pradesh"
    )

    print(coordinates)