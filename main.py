from datetime import datetime
from budget import (print_budget_summary, print_budget_status, suggest_budget_reduction)
from planner import get_destination_info
from exporter import save_trip_plan, print_itinerary
from itinerary import generate_itinerary


def print_trip_details(trip):
    print("\n" + "=" * 35)
    print("          TRIP DETAILS")
    print("=" * 35)

    print(f"From       : {trip['starting_location']}")
    print(f"To         : {trip['destination']}")
    print(f"Dates      : {trip['start_date']} - {trip['end_date']}")
    print(f"Travellers : {trip['travellers']}")
    print(f"Budget     : ₹{trip['budget']:,.2f}")
    print(f"Interests  : {trip['interests']}")
    print(f"Travel Days: {trip['travel_days']} days")
    print(f"Nights     : {trip['nights']} nights")

    print("=" * 35)

# Collect trip information
def get_trip_details():
    while True:

        try:
            trip = {
                "starting_location": input("Starting Location: ").strip(),
                "destination": input("Final Destination: ").strip().capitalize(),
                "state": input("State Of Destination: ").strip(),
                "start_date": input("Start Date: ").strip(),
                "end_date": input("End Date: ").strip(),
                "travellers": (input("No. of Travellers: ")),
                "budget": (input("Enter Your Budget: ")),
                "interests": input(
                        "Interests (nature, adventure, food, culture, shopping): ").strip(),
                "travel_style": input(
                        "Travel Style (budget, normal, luxury): "
                ).strip().lower()
            }


            try:
                trip["travellers"] = int(trip["travellers"])
                trip["budget"] = float(trip["budget"])

            except ValueError:
                raise ValueError(
                    "Travellers must be whole number and budget must be numeric"
                )

            try:
                start = datetime.strptime(trip["start_date"], "%d/%m/%Y")
                end = datetime.strptime(trip["end_date"], "%d/%m/%Y")

            except ValueError:
                raise ValueError(
                    "Dates must be valid and use the format of DD/MM/YYYY"
                )

            if not trip["starting_location"].strip():
                raise ValueError("Starting location cannot be empty.")

            if not trip["destination"].strip():
                raise ValueError("Destination cannot be empty.")

            if trip["travellers"] <= 0:
                raise ValueError("Number of travellers must be greater than 0.")

            if trip["budget"] <= 0:
                raise ValueError("Budget must be greater than 0.")

            if end < start:
                raise ValueError("End date cannot be before start date.")

            if end == start:
                raise ValueError("Trip must be at least 1 night long.")

            valid_styles = ["budget", "normal", "luxury"]

            if trip["travel_style"] not in valid_styles:
                raise ValueError(
                    "Travel style must be budget, normal, or luxury."
                )

            valid_interests = [
                "nature",
                "adventure",
                "food",
                "culture",
                "shopping"
            ]

            entered_interests = [
                interest.strip().lower()
                for interest in trip["interests"].split(",")
                if interest.strip()
            ]

            if not entered_interests:
                raise ValueError("Please enter at least one interest.")

            invalid_interests = [
                interest
                for interest in entered_interests
                if interest not in valid_interests
            ]

            if invalid_interests:
                raise ValueError(
                    "Invalid interest(s): "
                    + ", ".join(invalid_interests)
                    + ". Choose from nature, adventure, food, culture, shopping."
                )

            trip["interests"] = ", ".join(entered_interests)

            duration = end - start

            trip["nights"] = duration.days
            trip["travel_days"] = duration.days + 1 
            trip["travel_date"] = trip["start_date"]


            return trip

        except ValueError as error:
            print(f"Invalid Input: {error}")
            print("Please check the destination, state, and other details.")
            print("Restart the planner and try again.")

            return

def print_destination_info(destination_info):
        print("\n===== VERIFIED DESTINATION =====")
    
        print(f"Destination : {destination_info['destination']}")
        print(f"State       : {destination_info['state']}")
        print(f"Country     : {destination_info['country']}")
        print(f"Latitude    : {destination_info['coordinates']['latitude']}")
        print(f"Longitude   : {destination_info['coordinates']['longitude']}")
        print(f"Temperature : {destination_info['temperature']}°C")

        print("\nRoute Information:")
        print(
                f"Distance: "
                f"{destination_info['route_information']['distance_km']} km"
                )
        print(
                f"Estimated driving time: "
                f"{destination_info['route_information']['duration_hours']} hours"
                )

def main():

    print("\n" + "=" * 35)
    print("       AI TRAVEL PLANNER")
    print("=" * 35)

    # Get trip details from the user
    try:
        trip = get_trip_details()
        destination_info = get_destination_info(trip)

    except ValueError as error:
        print(f"\nInput Error: {error}")
        return

    except ConnectionError as error:
        print(f"\nNetwork Error: {error}")
        print("Please check your internet connection or try again later")
        return

    except Exception as error:
        print(f"Unexpected Error: {error}")
        return

    print("\n===== TRAVEL PREFERENCE =====")
    print(f"Travel Style: {trip['travel_style'].title()}")


    selected_interests = [
        interest.strip().lower()
        for interest in trip["interests"].split(",")
    ]

    print_destination_info(destination_info)


    print("\n===== TRANSPORT OPTIONS =====")

    for transport in destination_info["transport_options"]:
        print(f"Mode: {transport['mode']}")
        print(f"Provider: {transport['provider']}")
        print(f"From: {trip['starting_location']}")
        print(f"To: {trip['destination']}")
        print(f"Duration: {transport['duration_hours']} hours")
        print(f"Price per person: ₹{transport['price_per_person']}")
        print(f"Total price: ₹{transport['total_price']}")
        print()


    selected_transport = destination_info["selected_transport"]

    if selected_transport:
        print("\nSelected Transport:")
        print(f"Mode: {selected_transport.get('mode', 'N/A')}")
        print(f"Provider: {selected_transport.get('provider', 'N/A')}")
        print(f"From: {selected_transport.get('from_location', trip['starting_location'])}")
        print(f"To: {selected_transport.get('to_location', trip['destination'])}")
        print(f"Price per person: ₹{selected_transport.get('price_per_person', 'N/A')}")
        print(f"Total price: ₹{selected_transport.get('total_price', 'N/A')}")
    else:
        print("\nNo transport option selected.")


    print("\n===== ACCOMMODATION OPTIONS =====")

    for accommodation in destination_info["accommodation_options"]:
        print(f"Name: {accommodation['name']}")
        print(f"Location: {accommodation['location']}")
        print(f"Check-in: {accommodation['check_in']}")
        print(f"Check-out: {accommodation['check_out']}")
        print(f"Rooms: {accommodation['rooms']}")
        print(f"Price per night: ₹{accommodation['price_per_night']}")
        print(f"Total price: ₹{accommodation['total_price']}")
        print()

    selected_accommodation = destination_info["selected_accommodation"]

    if selected_accommodation:
        print("\nSelected Accommodation:")
        print(f"Name: {selected_accommodation.get('name', 'N/A')}")
        print(f"Location: {selected_accommodation.get('location', trip['destination'])}")
        print(f"Price per night: ₹{selected_accommodation.get('price_per_night', 'N/A')}")
        print(f"Total price: ₹{selected_accommodation.get('total_price', 'N/A')}")
    else:
        print("\nNo accommodation option selected.")

        
    # Display trip information
    print_trip_details(trip)

    # Display budget summary
    budget_plan = destination_info["budget_plan"]
    print_budget_summary(budget_plan)
    print_budget_status(budget_plan)

    suggest_budget_reduction(budget_plan)

    itinerary = generate_itinerary(trip,destination_info)
    save_trip_plan(trip,destination_info, itinerary)

    print_itinerary(itinerary)

    for day, details in itinerary.items():
        print(f"\n===== {day} =====")

        print("\nSightseeing:")
        for place in details.get("places", []):
            print(f"- {place['name']}")
            print(f"  Address: {place['address']}")

        print("\nFood:")
        for food in details.get("food", []):
            print(f"- {food['name']}")
            print(f"  Category: {food['category']}")
            print(f"  Address: {food['address']}")

        print("\nShopping:")
        for shopping in details.get("shopping", []):
            print(f"- {shopping['name']}")
            print(f"  Category: {shopping['category']}")
            print(f"  Address: {shopping['address']}")

if __name__ == "__main__":
    main()