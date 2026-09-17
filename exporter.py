def print_itinerary(itinerary):
    if not itinerary:
        print("No itinerary available.")
        return

    print("\n===== ITINERARY =====")

    for day, details in itinerary.items():
        print(f"\n{day}")
        print("-" * 30)

        print("Places to Visit:")

        if details.get("places"):
            for index, place in enumerate(details["places"], start=1):
                print(f"{index}. {place['name']}")
                print(f"   Address: {place['address']}")
                print(f"   Distance: {place['distance']}")
        else:
            print("No sightseeing places selected.")

        print("\nFood Places:")

        if details.get("food"):
            for index, food in enumerate(details["food"], start=1):
                print(f"{index}. {food['name']}")
                print(f"   Category: {food['category']}")
                print(f"   Address: {food['address']}")
                print(f"   Distance: {food['distance']}")
        else:
            print("No food places found.")