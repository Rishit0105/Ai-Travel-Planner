import requests

def get_weather(latitude,longitude):

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m"
            }
        )
    
    response.raise_for_status()

    data = response.json()
    temperature = data["current"]["temperature_2m"]

    return temperature

if __name__ == "__main__":

    temperature = get_weather(
        32.2574,
        77.17481
    )

    print(f"Current Temperature: {temperature}°C")