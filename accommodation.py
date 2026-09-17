from datetime import datetime


def get_accommodation_options(
    destination,
    check_in_date,
    check_out_date,
    travellers,
    budget
):

    check_in = datetime.strptime(check_in_date, "%d/%m/%Y")
    check_out = datetime.strptime(check_out_date, "%d/%m/%Y")

    nights = (check_out - check_in).days

    if nights <= 0:
        raise ValueError(
            "Check-out date must be after check-in date."
        )

    if travellers <= 0:
        raise ValueError(
            "Number of travellers must be greater than zero."
    )

    rooms = (travellers + 1) // 2

    return [
        {
            
        "name": "Budget Hotel",
        "location": destination,
        "check_in": check_in_date,
        "check_out": check_out_date,
        "price_per_night": 2500,
        "nights": nights,
        "rooms": rooms,
        "total_price": 2500 * nights * rooms,
        "currency": "INR"
        },

        {
            
        "name": "Comfort Hotel",
        "location": destination,
        "check_in": check_in_date,
        "check_out": check_out_date,
        "price_per_night": 4000,
        "nights": nights,
        "rooms": rooms,
        "total_price": 4000 * nights * rooms,
        "currency": "INR"
        },

        {
            
        "name": "Luxury Resort",
        "location": destination,
        "check_in": check_in_date,
        "check_out": check_out_date,
        "price_per_night": 7000,
        "nights": nights,
        "rooms": rooms,
        "total_price": 7000 * nights * rooms,
        "currency": "INR"
        }
]
    