def generate_itinerary(trip, destination_info):
    places = destination_info.get("places", [])
    food_places = destination_info.get("food", [])
    travel_days = trip.get("travel_days", 1)

    print("Number of food places:", len(food_places))

    interests = trip.get("interests", "")
    interests = [
        interest.strip().lower()
        for interest in interests.split(",")
        if interest.strip()
    ]

    itinerary = {
        f"Day {day}": {
            "places": [],
            "food": []
        }
        for day in range(1, travel_days + 1)
    }

    filtered_places = []

    for place in places:
        place_text = " ".join([
            str(place.get("name") or ""),
            str(place.get("address") or ""),
            str(place.get("category") or "")
        ]).lower()

        if not interests or any(
            interest in place_text for interest in interests
        ):
            filtered_places.append(place)

    if not filtered_places:
        filtered_places = places

    max_places_per_day = 3

    for index, place in enumerate(filtered_places):
        day_number = (index // max_places_per_day) + 1

        if day_number > travel_days:
            break

        day_key = f"Day {day_number}"

        itinerary[day_key]["places"].append({
            "name": place["name"],
            "address": place["address"],
            "distance": place.get("distance", "Unknown")
        })

    # Distribute food places across the days
    for index, food in enumerate(food_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["food"].append({
            "name": food["name"],
            "address": food["address"],
            "category": food.get("category") or "Food Place",
            "distance": food.get("distance", "Unknown")
        })

    return itinerary