from main import main
from exporter import load_trip_plan, print_loaded_trip, print_itinerary


def run_app():
    while True:
        print("\n===== AI TRAVEL PLANNER =====")
        print("1. Create a new trip")
        print("2. Load a saved trip")
        print("3. Exit")

        choice = input("Enter Your Choice: ").strip()

        if choice == "1":
            main()

        elif choice == "2":
            filename = input("Enter saved trip filename: ").strip()

            if not filename:
                print("Filename connot be empty.")
                continue

            trip_plan = load_trip_plan(filename)

            if trip_plan is not None:
                print_loaded_trip(trip_plan)
                print_itinerary(trip_plan.get("itinerary"))

            else:
                print("Could not load the saved trip.")

        elif choice == "3":
            print("Thank You For Using AI Travel Planner")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    run_app()