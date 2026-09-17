def generate_itinerary(trip, destination_info):
    places = destination_info.get("places", [])
    food_places = destination_info.get("food", [])
    shopping_places = destination_info.get("shopping", [])

    travel_days = trip.get("travel_days", 1)

    if travel_days <= 0:
        travel_days = 1

    print("Number of food places:", len(food_places))
    print("Number of shopping places:", len(shopping_places))

    interests = trip.get("interests", "")

    if isinstance(interests, str):
        interests = [
            interest.strip().lower()
            for interest in interests.split(",")
            if interest.strip()
        ]

    elif isinstance(interests, list):
        interests = [
            str(interest).strip().lower()
            for interest in interests
            if str(interest).strip()
        ]

    else:
        interests = []

    itinerary = {
        f"Day {day}": {
            "places": [],
            "food": [],
            "shopping": []
        }
        for day in range(1, travel_days + 1)
    }

    def matches_interests(item):
        if not interests:
            return True

        name = str(item.get("name") or "").lower()
        address = str(item.get("address") or "").lower()
        category = item.get("category") or ""

        if isinstance(category, list):
            category = " ".join(category)

        category = str(category).lower()

        searchable_text = f"{name} {address} {category}"

        return any(
            interest in searchable_text
            for interest in interests
        )

    # Filter sightseeing places
    filtered_places = [
        place
        for place in places
        if matches_interests(place)
    ]

    if not filtered_places:
        filtered_places = places

    # Distribute sightseeing across all days
    for index, place in enumerate(filtered_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["places"].append({
            "name": place.get("name", "Unknown Place"),
            "address": place.get("address", "Address unavailable"),
            "distance": place.get("distance", "Unknown")
        })

    # Distribute food places
    for index, food in enumerate(food_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["food"].append({
            "name": food.get("name", "Unknown Food Place"),
            "address": food.get("address", "Address unavailable"),
            "category": food.get("category") or "Food Place",
            "distance": food.get("distance", "Unknown")
        })

    # Distribute shopping places
    for index, shopping in enumerate(shopping_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["shopping"].append({
            "name": shopping.get(
                "name",
                "Unknown Shopping Place"
            ),
            "address": shopping.get(
                "address",
                "Address unavailable"
            ),
            "category": shopping.get(
                "category",
                "Shopping Place"
            ),
            "distance": shopping.get("distance", "Unknown")
        })

    return itinerary