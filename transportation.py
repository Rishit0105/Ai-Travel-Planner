from datetime import datetime
from flight_scraper import FlightScraper
from buses import get_live_buses
import re


AIRPORT_CODES = {
    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bombay": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "chennai": "MAA",
    "kolkata": "CCU",
    "hyderabad": "HYD",
    "pune": "PNQ",
    "ahmedabad": "AMD",
    "jaipur": "JAI",
    "lucknow": "LKO",
    "chandigarh": "IXC",
    "amritsar": "ATQ",
    "goa": "GOI",
    "srinagar": "SXR",
    "kochi": "COK",
    "coimbatore": "CJB",
    "bhubaneswar": "BBI",
    "patna": "PAT",
    "varanasi": "VNS",
    "indore": "IDR",
    "nagpur": "NAG",
    "surat": "STV",
    "dehradun": "DED",
    "guwahati": "GAU",
    "ranchi": "IXR",
    "chandigarh": "IXC",
    "jammu": "IXJ",
    "udaipur": "UDR",
    "jodhpur": "JDH",
    "goa": "GOI",
}


def get_airport_code(location):
    """
    Convert a city/location name into an IATA airport code.

    Returns None if the city is not currently supported.
    """

    if not location:
        return None

    location_clean = location.strip().lower()

    return AIRPORT_CODES.get(location_clean)


def _convert_duration_to_hours(duration_seconds):
    """
    Convert flight duration from seconds to hours.
    """

    if duration_seconds is None:
        return None

    return round(duration_seconds / 3600, 2)


def _get_flight_options(
    starting_location,
    destination,
    travel_date,
    travellers
):
    """
    Retrieve live flight options using Google Flights Selenium scraper.
    """

    scraper = None

    try:
        scraper = FlightScraper()

        formatted_date = datetime.strptime(
            travel_date,
            "%d/%m/%Y"
        ).strftime("%Y-%m-%d")

        flights = scraper.search_flights(
            source=starting_location,
            destination=destination,
            date=formatted_date
        )

        if not flights:
            print("\nNo live flights found.")
            return []

        flight_options = []

        for flight in flights[:10]:

            price_text = str(
                flight.get("price", "")
            )

            # Extract numeric price
            price_match = re.search(
                r"[\d,]+",
                price_text
            )

            if not price_match:
                continue

            total_price = int(
                price_match.group().replace(",", "")
            )

            # Scraper price is assumed to be per person
            price_per_person = total_price

            duration_text = flight.get(
                "duration",
                ""
            )

            duration_hours = 0

            duration_match = re.search(
                r"(\d+)\s*hr",
                duration_text
            )

            minutes_match = re.search(
                r"(\d+)\s*min",
                duration_text
            )

            if duration_match:
                duration_hours += int(
                    duration_match.group(1)
                )

            if minutes_match:
                duration_hours += round(
                    int(minutes_match.group(1)) / 60,
                    2
                )

            flight_options.append(
                {
                    "mode": "Flight",
                    "provider": flight.get(
                        "airline",
                        "Unknown Airline"
                    ),
                    "flight_number": flight.get(
                        "flight_number",
                        ""
                    ),
                    "duration_hours": duration_hours,
                    "duration": duration_text,
                    "price_per_person": price_per_person,
                    "total_price": (
                        price_per_person * travellers
                    ),
                    "currency": "INR",
                    "price_type": "Live",
                    "comfort_level": "High",
                    "booking_required": True,
                    "distance_km": None,
                    "route": (
                        f"{starting_location} to "
                        f"{destination}"
                    ),
                    "departure_time": flight.get(
                        "departure",
                        ""
                    ),
                    "arrival_time": flight.get(
                        "arrival",
                        ""
                    ),
                    "stops": flight.get(
                        "stops",
                        "Nonstop"
                    ),
                    "booking_link": (
                        "https://www.google.com/travel/flights"
                    ),
                    "price_level": None
                }
            )

        return flight_options

    except Exception as error:
        print(
            f"\nFlight scraper unavailable: {error}"
        )
        return []

    finally:
        if scraper:
            scraper.close()

def _get_bus_options(
        starting_location,
        destination,
        travel_date,
        travellers
):
    try:
        return get_live_buses(
            starting_location,
            destination,
            travel_date,
            travellers
        )

    except Exception as error:
        print(f"\nLive Bus API unavailable: {error}")

        return []


def calculate_approximate_price(options, travellers):
    if not options:
        return None

    prices = []

    for option in options:
        price = option.get("price_per_person")

        if price is not None:
            prices.append(price)

    if not prices:
        return None

    prices.sort()

    middle = len(prices) // 2

    if len(prices) % 2 == 0:
        approximate_price = (
            prices[middle - 1] + prices[middle]
        ) / 2

    else:
        approximate_price = prices[middle]

    return round(approximate_price)


def _get_estimated_train_options(
        starting_location,
        destination,
        travellers,
        distance_km,
        duration_hours
):
    train_price_per_person =   max(250, round(distance_km * 1.8))

    train_duration = max(1, round(duration_hours * 1.10, 1))

    return [
        {
            "mode": "Train",
            "provider": "Estimated Train Service",
            "duration_hours": train_duration,
            "price_per_person": train_price_per_person,
            "total_price": train_price_per_person * travellers,
            "currency": "INR",
            "price_type": "Estimated",
            "comfort_level": "High",
            "booking_required": True,
            "distance_km": distance_km,
            "route": f"{starting_location} to {destination}"
        }
    ]


def _get_estimated_cab_options(
        starting_location,
        destination,
        travellers,
        distance_km,
        duration_hours
):
    cab_total_price = max(1200, round(distance_km * 12))

    cab_duration = max(1 , round(duration_hours, 1))

    return [
        {
            "mode": "Cab",
            "provider": "Estimated Cab Service",
            "duration_hours": cab_duration,
            "price_per_person": round(
                cab_total_price / travellers
            ),
            "total_price": cab_total_price,
            "currency": "INR",
            "price_type": "Estimated",
            "comfort_level": "High",
            "booking_required": True,
            "distance_km": distance_km,
            "route": f"{starting_location} to {destination}"
        }
    ]


def get_transport_estimates(
        starting_location,
        destination,
        travel_date,
        travellers,
        route_information = None
):
    if travellers <= 0:
        raise ValueError(
            "Number of travellers must be greater than 0."
        )

    if not travel_date.strip():
        raise ValueError(
            "Travel date cannot be empty."
        )

    if not starting_location.strip():
        raise ValueError(
            "Starting Location cannot be empty."
        )

    if not destination.strip():
        raise ValueError(
            "Destination cannot be empty."
        )

    if not route_information:
        raise ValueError(
            "Route information is required for transport estimation."
        )

    distance_km = route_information.get("distance_km")
    duration_hours = route_information.get("duration_hours")

    if not distance_km or distance_km <= 0:
        raise ValueError(
            "Valid route distance is required for transport estimation."
        )

    if not duration_hours or duration_hours <= 0:
        duration_hours = distance_km / 60

    train_options = _get_estimated_train_options(
        starting_location,
        destination,
        travellers,
        distance_km,
        duration_hours
    )

    cab_options = _get_estimated_cab_options(
        starting_location,
        destination,
        travellers,
        distance_km,
        duration_hours
    )

    bus_options = _get_bus_options(
        starting_location,
        destination,
        travel_date,
        travellers
    )

    if not bus_options:
        bus_price_per_person = max(
            300,
            round(distance_km * 2.5)
        )

        bus_duration = max(
            1,
            round(duration_hours * 1.25, 1)
        )

        bus_options = [
            {
                "mode": "Bus",
                "provider": "Estimated Bus Service",
                "duration_hours": bus_duration,
                "price_per_person": bus_price_per_person,
                "total_price": (
                    bus_price_per_person * travellers
                ),
                "currency": "INR",
                "price_type": "Estimated",
                "comfort_level": "Medium",
                "booking_required": True,
                "distance_km": distance_km,
                "route": (
                    f"{starting_location} to "
                    f"{destination}"
                )
            }
        ]

    flight_options = _get_flight_options(
        starting_location,
        destination,
        travel_date,
        travellers
    )

    if not flight_options:
        flight_options = []

    estimates = {}

    estimates["Bus"] = {
        "approx_price": calculate_approximate_price(
            bus_options,
            travellers
            ),
        "price_type": (
            "Live"
            if any(
                option.get("price_type") == "Live"
                for option in bus_options
            )
            else "Estimated"
        )
    }

    estimates["Train"] = {
        "approx_price": calculate_approximate_price(
            train_options,
            travellers
        ),
        "price_type": "Estimated"
    }

    estimates["Cab"] = {
        "approx_price": calculate_approximate_price(
            cab_options,
            travellers
        ),
        "price_type": "Estimated"
    }

    estimates["Flight"] = {
        "approx_price": calculate_approximate_price(
            flight_options,
            travellers
        ),
        "price_type": (
            "Live"
            if flight_options
            else "Unavailable"
        )
    }

    return estimates


def get_transport_options(
    mode,
    starting_location,
    destination,
    travel_date,
    travellers,
    route_information=None
):
    if travellers <= 0:
        raise ValueError(
            "Number of travellers must be greater than zero."
        )

    if not travel_date.strip():
        raise ValueError(
            "Travel date cannot be empty."
        )

    if not starting_location.strip():
        raise ValueError(
            "Starting location cannot be empty."
        )

    if not destination.strip():
        raise ValueError(
            "Destination cannot be empty."
        )

    distance_km = None
    duration_hours = None

    if route_information:
        distance_km = route_information.get(
            "distance_km"
        )

        duration_hours = route_information.get(
            "duration_hours"
        )

    if not distance_km or distance_km <= 0:
        raise ValueError(
            "Valid route distance is required "
            "for transport estimation."
        )

    if not duration_hours or duration_hours <= 0:
        duration_hours = distance_km / 60

    mode = mode.strip().lower()

    if mode == "flight":
        return _get_flight_options(
            starting_location,
            destination,
            travel_date,
            travellers
        )

    elif mode == "bus":
        bus_options = _get_bus_options(
            starting_location,
            destination,
            travel_date,
            travellers
        )

        if bus_options:
            return bus_options

        # Fallback to estimated bus
        bus_price_per_person = max(
            300,
            round(distance_km * 2.5)
        )

        bus_duration = max(
            1,
            round(duration_hours * 1.25, 1)
        )

        return [
            {
                "mode": "Bus",
                "provider": "Estimated Bus Service",
                "duration_hours": bus_duration,
                "price_per_person": bus_price_per_person,
                "total_price": (
                    bus_price_per_person * travellers
                ),
                "currency": "INR",
                "price_type": "Estimated",
                "comfort_level": "Medium",
                "booking_required": True,
                "distance_km": distance_km,
                "route": (
                    f"{starting_location} to "
                    f"{destination}"
                )
            }
        ]

    elif mode == "train":
        return _get_estimated_train_options(
            starting_location,
            destination,
            travellers,
            distance_km,
            duration_hours
        )

    elif mode == "cab":
        return _get_estimated_cab_options(
            starting_location,
            destination,
            travellers,
            distance_km,
            duration_hours
        )

    else:
        raise ValueError(
            f"Unsupported transport mode: {mode}"
        )
    
if __name__ == "__main__":
    test_route = {
        "distance_km": 303.51,
        "duration_hours": 4.55
    }

    estimates = get_transport_estimates(
        starting_location="Delhi",
        destination="Jaipur",
        travel_date="20/10/2026",
        travellers=1,
        route_information=test_route
    )

    print("\n" + "=" * 50)
    print("TRANSPORT PRICE ESTIMATES")
    print("=" * 50)

    for mode, data in estimates.items():
        print(
            f"{mode}: "
            f"₹{data['approx_price']:,} "
            f"({data['price_type']})"
        )