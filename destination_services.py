from geocoding_api import get_coordinates
from weather_api import get_weather

def get_destination_services(destination , state=None):

    coordinates = get_coordinates(destination , state)

    temperature = get_weather(
        coordinates["latitude"],
        coordinates["longitude"]
    )

    return {
        "destination": coordinates["name"],
        "state": coordinates["state"],
        "country": coordinates["country"],
        "coordinates": {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"]
        },
        "temperature": temperature
    }

if __name__ == "__main__":

    destination_info = get_destination_services(
        "Manali",
        "Himachal Pradesh"
    )

    print(destination_info)