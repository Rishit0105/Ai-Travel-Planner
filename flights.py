import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "google-flights-live-api.p.rapidapi.com"
ONEWAY_URL = f"https://{API_HOST}/api/google_flights/oneway/v1"
ROUNDTRIP_URL = f"https://{API_HOST}/api/google_flights/roundtrip/v1"


def _check_api_key():
    if not RAPIDAPI_KEY:
        raise ValueError("RAPIDAPI_KEY is missing. Add it to your .env file.")


def _headers():
    return {
        "Content-Type": "application/json",
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
    }


def _extract_results(data):
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        return []

    for key in ("flights", "itineraries", "results", "data"):
        value = data.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            for nested_key in ("flights", "itineraries", "results", "topFlights"):
                nested = value.get(nested_key)
                if isinstance(nested, list):
                    return nested
    return []


def _number(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        cleaned = value.replace(",", "").replace("₹", "").replace("$", "").replace("€", "").replace("£", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def _normalize_flight(flight):
    if not isinstance(flight, dict):
        return None

    price = (
        flight.get("price_as_number")
        or flight.get("total_price_as_number")
        or _number(flight.get("price"))
        or _number(flight.get("total_price"))
    )

    airline = flight.get("airline") or flight.get("airlines") or flight.get("carrier") or "Unknown Airline"
    if isinstance(airline, list):
        airline = ", ".join(str(x) for x in airline)

    return {
        "airline": airline,
        "price": price,
        "price_display": flight.get("price") or flight.get("total_price"),
        "departure_time": flight.get("departure_time"),
        "arrival_time": flight.get("arrival_time"),
        "duration_minutes": flight.get("duration_minutes") or flight.get("duration"),
        "stops": flight.get("stops") if flight.get("stops") is not None else flight.get("number_of_stops"),
        "departure_airport": flight.get("departure_airport") or flight.get("from_airport"),
        "arrival_airport": flight.get("arrival_airport") or flight.get("to_airport"),
        "booking_link": flight.get("buy_link") or flight.get("booking_link") or flight.get("book_link"),
        "price_verdict": flight.get("price_range_in_relation_to_other_periods") or flight.get("price_verdict"),
        "raw": flight,
    }


def _request(url, payload):
    _check_api_key()

    response = requests.post(
        url,
        headers=_headers(),
        json=payload,
        timeout=30,
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()


def get_one_way_flights(from_airport, to_airport, departure_date, adults=1,
                        travel_class="ECONOMY", currency="INR",
                        max_stops=None, limit=5):
    payload = {
    "from_airport": from_airport.upper(),
    "to_airport": to_airport.upper(),
    "departure_date": departure_date,
    "limit": limit,
    "currency": currency.lower(),
    "passengers": [1] * adults,
    "seat_type": 1 if travel_class.upper() == "ECONOMY" else 3,
}

    if max_stops is not None:
        payload["max_stops"] = max_stops

    data = _request(ONEWAY_URL, payload)
    flights = [_normalize_flight(x) for x in _extract_results(data)]
    flights = [x for x in flights if x]

    return sorted(
        flights,
        key=lambda x: (x["price"] is None, x["price"] if x["price"] is not None else float("inf"))
    )


def get_round_trip_flights(from_airport, to_airport, departure_date, return_date,
                           adults=1, travel_class="ECONOMY", currency="INR",
                           max_stops=None, limit=5):
    payload = {
    "from_airport": from_airport.upper(),
    "to_airport": to_airport.upper(),
    "departure_date": departure_date,
    "limit": limit,
    "currency": currency.lower(),
    "passengers": [1] * adults,
    "seat_type": 1 if travel_class.upper() == "ECONOMY" else 3,
}


    data = _request(ROUNDTRIP_URL, payload)
    flights = [_normalize_flight(x) for x in _extract_results(data)]
    flights = [x for x in flights if x]

    return sorted(
        flights,
        key=lambda x: (x["price"] is None, x["price"] if x["price"] is not None else float("inf"))
    )


def print_flights(flights):
    if not flights:
        print("\nNo flights found.")
        return

    print("\n===== FLIGHT OPTIONS =====")

    for i, flight in enumerate(flights, 1):
        print(f"\nFlight {i}")
        print(f"Airline: {flight['airline']}")

        if flight["price"] is not None:
            print(f"Price: ₹{flight['price']:,.0f}")
        elif flight["price_display"]:
            print(f"Price: {flight['price_display']}")

        if flight["departure_time"]:
            print(f"Departure: {flight['departure_time']}")
        if flight["arrival_time"]:
            print(f"Arrival: {flight['arrival_time']}")
        if flight["duration_minutes"] is not None:
            print(f"Duration: {flight['duration_minutes']}")
        if flight["stops"] is not None:
            print(f"Stops: {flight['stops']}")
        if flight["price_verdict"]:
            print(f"Price level: {flight['price_verdict']}")
        if flight["booking_link"]:
            print(f"Booking: {flight['booking_link']}")


if __name__ == "__main__":
    flights = get_one_way_flights(
        from_airport="DEL",
        to_airport="GOI",
        departure_date="2026-10-20",
        adults=2,
        travel_class="ECONOMY",
        currency="INR",
        limit=5,
    )
    print_flights(flights)
