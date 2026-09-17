import requests


def get_transport_options(
    starting_location,
    destination,
    travel_date,
    travellers
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

    try:
        # Keep your current mock return here temporarily
        return [
            {
                "mode": "Bus",
                "provider": "Example Bus",
                "duration_hours": 7,
                "price_per_person": 800,
                "total_price": 800 * travellers,
                "currency": "INR"
            }
        ]

    except requests.exceptions.RequestException:
        raise ConnectionError(
            "Unable to connect to the transport service."
        )