def filter_places_by_interest(places, interests):

    if isinstance(interests, str):
        interests = interests.split(",")

    interests = [
        interest.strip().lower()
        for interest in interests
        if interest.strip()
    ]

    interest_keywords = {
        "nature": [
            "park",
            "garden",
            "lake",
            "river",
            "forest",
            "mountain",
            "hill",
            "valley",
            "waterfall",
            "viewpoint",
            "zoo",
            "botanical",
            "nature",
            "wildlife",
            "reserve",
            "eco"
        ],

        "adventure": [
            "trek",
            "trail",
            "camp",
            "camping",
            "hiking",
            "climbing",
            "rafting",
            "adventure",
            "waterfall",
            "mountain",
            "hill",
            "viewpoint",
            "valley"
        ],

        "culture": [
            "temple",
            "museum",
            "palace",
            "monument",
            "fort",
            "monastery",
            "church",
            "mosque",
            "shrine",
            "heritage",
            "historical",
            "historic",
            "gallery",
            "castle"
        ],

        "shopping": [
            "mall",
            "market",
            "bazaar",
            "street",
            "shop",
            "shopping",
            "emporium",
            "retail"
        ]
    }

    filtered_places = []
    added_place_names = set()

    for place in places:

        name = str(place.get("name") or "").lower()
        address = str(place.get("address") or "").lower()

        raw_category = place.get("category", "")

        if isinstance(raw_category, list):
            category = " ".join(raw_category).lower()
            
        else:
            category = str(raw_category or "").lower()

        searchable_text = f"{name} {address} {category}"

        for interest in interests:

            keywords = interest_keywords.get(
                interest,
                [interest]
            )

            if any(
                keyword in searchable_text
                for keyword in keywords
            ):

                place_name = name.strip()

                if place_name not in added_place_names:
                    filtered_places.append(place)
                    added_place_names.add(place_name)

                break

    print("\n===== FILTER DEBUG =====")
    print("Requested Interests:", interests)
    print("Total Places Received:", len(places))
    print("Places after filtering:", len(filtered_places))

    for place in filtered_places:
        print("-", place.get("name"))

    return filtered_places