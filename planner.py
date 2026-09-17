from destination_services import get_destination_services
from places import get_places
from food import get_food_places
from interest_filter import filter_places_by_interest
from shopping import get_shopping_places
from transportation import get_transport_options
from accommodation import get_accommodation_options
from option_selector import (filter_transport_options,
                             filter_accommodation_options,
                             select_transport_options,
                             select_accommodation_options,
                             select_option_within_budget
                            )
from routing import get_route_information
from budget import calculate_budget, suggest_budget_reduction


def get_destination_info(trip):

    destination = trip["destination"]
    state = trip.get("state")

    # Get destination services first
    services = get_destination_services(
        destination,
        state
    )

    latitude = services["coordinates"]["latitude"]
    longitude = services["coordinates"]["longitude"]

    # Transportation
    transport_options = get_transport_options(
        trip["starting_location"],
        destination,
        trip["travel_date"],
        trip["travellers"]
    )

    route_information = get_route_information(
        trip["starting_location"],
        destination
    )

    transport_options = filter_transport_options(
        transport_options,
        trip["travel_style"]
    )

    # Accommodation
    accommodation_options = get_accommodation_options(
        destination,
        trip["start_date"],
        trip["end_date"],
        trip["travellers"],
        trip["budget"]
    )

    accommodation_options = filter_accommodation_options(
        accommodation_options,
        trip["travel_style"]
    )

    # Select transportation
    selected_transport = select_option_within_budget(
        transport_options,
        trip["budget"] * 0.30
    )

    if selected_transport is None and transport_options:
        selected_transport = min(
            transport_options,
            key=lambda transport: transport["total_price"]
        )

    # Select accommodation
    accommodation_budget = trip["budget"] * 0.30

    if trip["travel_style"].lower() == "luxury":
        if accommodation_options:
            selected_accommodation = max(
                accommodation_options,
                key=lambda accommodation: accommodation["total_price"]
            )
        else:
            selected_accommodation = None

    else:
        selected_accommodation = select_option_within_budget(
            accommodation_options,
            accommodation_budget
        )

        if selected_accommodation is None and accommodation_options:
            selected_accommodation = min(
                accommodation_options,
                key=lambda accommodation: accommodation["total_price"]
            )

    if selected_transport is None:
        print(
            "\nNo transport option was found within the transport budget"
        )

    if selected_accommodation is None:
        print(
            "\nNo accommodation option was found within the accommodation budget"
        )

    # Budget calculation
    budget_plan = calculate_budget(
        trip,
        selected_transport,
        selected_accommodation
    )

    suggest_budget_reduction(budget_plan)

    # Sightseeing places
    places = get_places(
        latitude,
        longitude
    )

    tourist_interests = ",".join(
        interest.strip()
        for interest in trip["interests"].split(",")
        if interest.strip().lower() not in ["food", "shopping"]
    )

    filtered_places = filter_places_by_interest(
        places,
        tourist_interests
    )

    # Selected interests
    selected_interests = [
        interest.strip().lower()
        for interest in trip["interests"].split(",")
        if interest.strip()
    ]

    # Food places
    if "food" in selected_interests:
        food_places = get_food_places(
            latitude,
            longitude
        )
    else:
        food_places = []

    # Shopping places
    if "shopping" in selected_interests:
        shopping_places = get_shopping_places(
            latitude,
            longitude
        )
    else:
        shopping_places = []

    # Build destination_info only after collecting all data
    destination_info = {
        "destination": services["destination"],
        "state": services["state"],
        "country": services["country"],
        "coordinates": services["coordinates"],
        "temperature": services["temperature"],
        "places": filtered_places,
        "treks": [],
        "food": food_places,
        "shopping": shopping_places,
        "transport_options": transport_options,
        "accommodation_options": accommodation_options,
        "selected_transport": selected_transport,
        "selected_accommodation": selected_accommodation,
        "route_information": route_information,
        "budget_plan": budget_plan
    }

    return destination_info