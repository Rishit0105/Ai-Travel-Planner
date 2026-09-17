def get_travel_style_preferences(travel_style):

    preferences = {
        "budget": {
            "max_price_multiplier": 1.0,
            "priority": "price"
        },

        "normal": {
            "max_price_multiplier": 1.5,
            "priority": "balanced"
        },

        "luxury": {
            "max_price_multiplier": 3.0,
            "priority": "comfort"
        }
    }

    if travel_style not in preferences:
        raise ValueError(
            "Travel style must be budget, normal, or luxury."
        )

    return preferences[travel_style]


def filter_transport_options(
        transport_options,
        travel_style
):

    preferences = get_travel_style_preferences(travel_style)

    if not transport_options:
        return []

    cheapest_price = min(
                option["total_price"]
                for option in transport_options
                )

    max_allowed_price = (
        cheapest_price * preferences["max_price_multiplier"]
    )

    filtered_options = [
        option
        for option in transport_options
        if option["total_price"] <= max_allowed_price
    ]

    return filtered_options


def filter_accommodation_options(
        accommodation_options,
        travel_style
):

    preferences = get_travel_style_preferences(travel_style)

    if not accommodation_options:
        return []

    cheapest_price = min(
                option["total_price"]
                for option in accommodation_options
                )

    max_allowed_price = (
        cheapest_price * preferences["max_price_multiplier"]
    )

    filtered_options = [
        option
        for option in accommodation_options
        if option["total_price"] <= max_allowed_price
    ]

    return filtered_options


def select_cheapest_option(options):
    if not options:
        return None

    return min(
        options,
        key=lambda option: option["total_price"]
    )


def select_option_within_budget(options, max_budget):
    if not options:
        return None

    affordable_options = [
        option
        for option in options
        if option["total_price"] <= max_budget
    ]

    if not affordable_options:
        return None

    return min(
        affordable_options,
        key=lambda option: option["total_price"]
    )


def select_transport_options(transport_options):
    return select_cheapest_option(transport_options)


def select_accommodation_options(accommodation_options):
    return select_cheapest_option(accommodation_options)