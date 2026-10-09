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

    def get_searchable_text(item):
        name = str(item.get("name") or "").lower()
        address = str(item.get("address") or "").lower()
        category = item.get("category") or ""

        if isinstance(category, list):
            category = " ".join(category)

        category = str(category).lower()

        return f"{name} {address} {category}"

    def matches_interests(item):
        if not interests:
            return True

        searchable_text = get_searchable_text(item)

        return any(
            interest in searchable_text
            for interest in interests
        )

    def get_area(item):
        """
        Attempts to identify the area of a place using its
        name and address.

        These keywords are especially useful for Jaipur.
        Unknown places are placed in a general group.
        """

        searchable_text = get_searchable_text(item)

        area_keywords = {
            "Amer Area": [
                "amer",
                "amber",
                "fort",
                "ganesh pol",
                "sheesh mahal",
                "panna meena",
                "jaigarh",
                "nahargarh"
            ],
            "Central Jaipur": [
                "city palace",
                "diwan-i-khas",
                "diwan e khas",
                "jantar mantar",
                "hawa mahal",
                "pink city",
                "bapu bazaar",
                "johari bazaar",
                "tripolia bazaar",
                "paanch batti"
            ],
            "Gaitor Area": [
                "gaitor",
                "royal gaitor",
                "garh ganesh"
            ],
            "City Area": [
                "shaheed smarak",
                "central park",
                "ram niwas",
                "albert hall",
                "museum",
                "railway station",
                "bani park"
            ],
            "Shopping Area": [
                "market",
                "bazaar",
                "mall",
                "shopping",
                "marketplace",
                "emporium",
                "souvenir"
            ]
        }

        for area, keywords in area_keywords.items():
            if any(keyword in searchable_text for keyword in keywords):
                return area

        return "General Area"

    def prepare_item(item, item_type):
        if item_type in ["place", "places"]:
            return {
                "name": item.get("name", "Unknown Place"),
                "address": item.get(
                    "address",
                    "Address unavailable"
                ),
                "distance": item.get("distance", "Unknown")
            }

        if item_type == "food":
            return {
                "name": item.get("name", "Unknown Food Place"),
                "address": item.get(
                    "address",
                    "Address unavailable"
                ),
                "category": item.get("category") or "Food Place",
                "distance": item.get("distance", "Unknown")
            }

        if item_type == "shopping":
            return {
                "name": item.get("name", "Unknown Shopping Place"),
                "address": item.get(
                    "address",
                    "Address unavailable"
                ),
                "category": item.get(
                    "category",
                    "Shopping Place"
                ),
                "distance": item.get("distance", "Unknown")
            }

    def group_by_area(items):
        grouped_items = {}

        for item in items:
            area = get_area(item)

            if area not in grouped_items:
                grouped_items[area] = []

            grouped_items[area].append(item)

        return grouped_items

    def distribute_groups(grouped_items, item_type):
        """
        Assigns each area group to a day.

        The largest group is assigned first to keep the
        itinerary relatively balanced.
        """

        sorted_groups = sorted(
            grouped_items.items(),
            key=lambda group: len(group[1]),
            reverse=True
        )

        day_loads = {
            day: 0
            for day in range(1, travel_days + 1)
        }

        for area, area_items in sorted_groups:
            target_day = min(
                day_loads,
                key=day_loads.get
            )

            day_key = f"Day {target_day}"

            for item in area_items:
                itinerary[day_key][item_type].append(
                    prepare_item(item, item_type)
                )

            day_loads[target_day] += len(area_items)

    # Filter sightseeing places according to interests
    filtered_places = [
        place
        for place in places
        if matches_interests(place)
    ]

    # If filtering removes everything, use all places
    if not filtered_places:
        filtered_places = places

    # Group sightseeing places by area
    place_groups = group_by_area(filtered_places)

    # Assign sightseeing groups to days
    distribute_groups(place_groups, "places")

    # Distribute food places individually across the days
    for index, food in enumerate(food_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["food"].append(
            prepare_item(food, "food")
        )

    # Distribute shopping places individually across the days
    for index, shopping in enumerate(shopping_places):
        day_number = (index % travel_days) + 1
        day_key = f"Day {day_number}"

        itinerary[day_key]["shopping"].append(
            prepare_item(shopping, "shopping")
        )
    return itinerary