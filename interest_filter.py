def filter_places_by_interest(places, interests):

    interests = [
        interest.strip().lower()
        for interest in interests.split(",")
    ]

    interest_keywords = {
        "nature": [
            "valley",
            "waterfall",
            "viewpoint",
            "lake",
            "river",
            "forest",
            "garden",
            "mountain"
        ],

        "adventure": [
            "trek",
            "trail",
            "waterfall",
            "mountain",
            "viewpoint",
            "valley"
        ],

        "culture": [
            "temple",
            "museum",
            "palace",
            "monastery",
            "church"
        ],

        "shopping": [
            "mall",
            "market",
            "bazaar",
            "street",
            "shop"
        ]
    }

    filtered_places = []

    for place in places:

        name = (place.get("name") or "").lower()
        address = (place.get("address") or "").lower()

        searchable_text = f"{name} {address}"

        for interest in interests:

            keywords = interest_keywords.get(
                interest,
                [interest]
            )

            if any(
                keyword in searchable_text
                for keyword in keywords
            ):
                filtered_places.append(place)
                break

    return filtered_places