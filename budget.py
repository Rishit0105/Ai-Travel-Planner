def get_budget_status(remaining_budget, budget):

    if remaining_budget < 0:
        return "Over Budget"

    elif remaining_budget < budget * 0.10:
        return "Almost Over Budget"

    elif remaining_budget == budget:
        return "Budget Fully Used"

    else:
        return "Within Budget"

def get_daily_estimates(travel_style):
    estimates = {
        "budget":{
            "food_per_person": 500,
            "activities_per_person": 300
        },

        "normal":{
            "food_per_person": 800,
            "activities_per_person": 500
        },

        "luxury":{
            "food_per_person": 1500,
            "activities_per_person": 1000
        }
    }

    return estimates.get(
        travel_style.lower(),
        estimates["normal"]
    )

def print_budget_summary(budget_plan):
    print("\n===== BUDGET SUMMARY =====")
    print(
        f"Transportation : ₹{budget_plan['transportation']:.2f}"
    )
    print(
        f"Accommodation  : ₹{budget_plan['accommodation']:.2f}"
    )
    print(
        f"Food           : ₹{budget_plan['food']:.2f}"
    )
    print(
        f"Activities     : ₹{budget_plan['activities']:.2f}"
    )
    print(
        f"Emergency      : ₹{budget_plan['emergency']:.2f}"
    )
    print("--------------------------")
    print(
        f"Estimated Total : ₹{budget_plan['total_estimated']:.2f}"
    )
    print(
        f"Remaining Budget: ₹{budget_plan['remaining_budget']:.2f}"
    )
    print(
        f"Budget Status   : {budget_plan['budget_status']}"
    )
    print(
        f"Budget Used     : "
        f"{budget_plan['budget_percentage_used']:.2f}%"
    )
    print(
        f"Warning         : {budget_plan['budget_warning']}"
    )
    print(
        f"Highest Expense : "
        f"{budget_plan['highest_expense_category']} "
        f"(₹{budget_plan['highest_expense_amount']:.2f})"
    )


def calculate_budget(trip, selected_transport=None, selected_accommodation=None):

    budget = trip["budget"]
    travellers = trip["travellers"]
    nights = trip["nights"]
    travel_days = trip["travel_days"]

    travel_style = trip["travel_style"]
    daily_estimates = get_daily_estimates(travel_style)

    # Default temporary estimates
    transportation = 3000 * travellers
    accommodation = 2500 * nights
    food = (
        daily_estimates["food_per_person"]
        * travellers
        * travel_days
    )
    
    activities = (
        daily_estimates["activities_per_person"]
        *travellers
        *travel_days
    )

    # Use actual transport price if available
    if selected_transport:
        transportation = selected_transport["total_price"]

    # Use actual accommodation price if available
    if selected_accommodation:
        accommodation = selected_accommodation["total_price"]

    # Emergency reserve
    subtotal = transportation + accommodation + food + activities
    emergency = subtotal * 0.10

    total_estimated = (
        transportation
        + accommodation
        + food
        + activities
        + emergency
    )

    expense_categories = {
        "Transportation": transportation,
        "Accommodation": accommodation,
        "Food": food,
        "Activities": activities,
        "Emergency": emergency 
    }

    highest_expense_category = max(
        expense_categories,
        key=expense_categories.get
    )

    highest_expense_amount = expense_categories[
        highest_expense_category
    ]

    budget_percentage_used = (
        total_estimated / budget
    ) * 100

    if budget_percentage_used > 100:
        budget_warning = (
            "Your estimated trip cost exceeds your budget "
            "Consider cheaper transport, accommodation or activities"
        )

    elif(budget_percentage_used >= 90):
        budget_warning = (
            "You are close to your budget limit "
            "Keep some extra money available"
        )

    elif(budget_percentage_used == 100):
        budget_warning = (
            "Your entire budget is allocated"
            "Keep extra money available for unexpected expenses."
        )

    else: 
        budget_warning = (
            "Your estimated trip is comfortably within budget"
        )

    remaining_budget = budget - total_estimated

    budget_status = get_budget_status(
        remaining_budget,
        budget
    )

    return {
        "transportation": transportation,
        "accommodation": accommodation,
        "food": food,
        "activities": activities,
        "emergency": emergency,
        "total_estimated": total_estimated,
        "highest_expense_category": highest_expense_category,
        "highest_expense_amount": highest_expense_amount,
        "budget_percentage_used": budget_percentage_used,
        "budget_warning": budget_warning,
        "remaining_budget": remaining_budget,
        "budget_status": budget_status
    }


def print_budget_status(budget_plan):
    print("\n===== BUDGET STATUS =====")
    print(f"Budget Status: {budget_plan['budget_status']}")
    print(f"Estimated Cost: ₹{budget_plan['total_estimated']:.2f}")
    print(f"Budget Used: {budget_plan['budget_percentage_used']:.2f}%")
    print(f"Remaining Budget: ₹{budget_plan['remaining_budget']:.2f}")

    if budget_plan["budget_status"] == "Over Budget":
        print("\nWARNING:")
        print(budget_plan["budget_warning"])

    elif budget_plan["budget_status"] == "Almost Over Budget":
        print("\nWARNING:")
        print(budget_plan["budget_warning"])

    else:
        print("\nYour trip is within the budget.")


def suggest_budget_reduction(budget_plan):
    if budget_plan["budget_status"] != "Over Budget":
        print("\n Your current plan doesnt require budget reduction")
        return 
    
    excess_amount  = abs(budget_plan["remaining_budget"])

    print("\n===== BUDGET RECOMMENDATION =====")
    print(f"You need to reduce approximately ₹{excess_amount:.2f}.")

    print(
        f"Largest expense: "
        f"{budget_plan['highest_expense_category']}"
        f"(₹{budget_plan['highest_expense_amount']:.2f})"
    )

    print("\nRecommended actions:")

    if budget_plan["highest_expense_category"] == "Transportation":
        print("1. Choose a cheaper transport option.")
        print("2. Compare bus, train, and flight prices.")
        print("3. Consider travelling on a cheaper date.")

    elif budget_plan["highest_expense_category"] == "Accommodation":
        print("1. Choose cheaper accommodation.")
        print("2. Reduce the number of nights.")
        print("3. Consider hostels or budget stays.")

    elif budget_plan["highest_expense_category"] == "Food":
        print("1. Reduce daily food spending.")
        print("2. Choose affordable restaurants.")
        print("3. Prefer included hotel meals where available.")

    elif budget_plan["highest_expense_category"] == "Activities":
        print("1. Reduce paid activities.")
        print("2. Prefer free sightseeing locations.")
        print("3. Remove optional activities.")

    else:
        print("1. Review all expense categories.")
        print("2. Reduce optional spending.")
