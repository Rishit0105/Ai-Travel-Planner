import json


def save_trip_plan(trip_plan, filename="trip_plan.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(trip_plan, file, indent=4, ensure_ascii=False)

    print(f"Trip plan saved to {filename}")


def load_trip_plan(filename="trip_plan.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                trip_plan = json.load(file)

            print(f"Trip plan loaded from {filename}")
            return trip_plan

        except FileNotFoundError:
            print(f"No saved trip plan found at {filename}")
            return None


def print_loaded_trip(trip_plan):
    if not trip_plan:
        print("No saved trip plan available.")
        return

    print("\n===== LOADED TRIP PLAN =====")

    for key, value in trip_plan.items():
        if key == "itinerary":
            continue

        print(f"{key}: {value}")

    if trip_plan.get("itinerary"):
        print_itinerary(trip_plan["itinerary"])


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