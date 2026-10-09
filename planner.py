from destination_services import get_destination_services
from places import get_places
from food import get_food_places
from interest_filter import filter_places_by_interest
from shopping import get_shopping_places
from transportation import get_transport_estimates, get_transport_options
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
    # Route information must be fetched first
    route_information = get_route_information(
        trip["starting_location"],
        destination,
        state
    )   

    # Transportation options use the real route distance
    all_transport_options = get_transport_estimates(
    trip["starting_location"],
    trip["destination"],
    trip["start_date"],
    trip["travellers"],
    route_information
    )   

    selected_transport = None

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

    if selected_accommodation is None:
        print(
            "\nNo accommodation option was found within the accommodation budget"
        )

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

    if len(filtered_places) < min(5, len(places)):
        filtered_places = places

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
        "transport_estimates": all_transport_options,
        "recommended_transport_budget": trip["budget"] * 0.30,
        "accommodation_options": accommodation_options,
        "selected_transport": None,
        "selected_accommodation": selected_accommodation,
        "route_information": route_information
    }

    return destination_info