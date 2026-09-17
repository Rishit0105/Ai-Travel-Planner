# AI Travel Planner ✈️

An intelligent Python-based travel planning application that helps users generate personalized trip plans based on their destination, travel dates, number of travelers, budget, travel style, and interests.

The application combines destination information, weather data, route details, sightseeing places, food recommendations, shopping locations, accommodation estimates, and budget planning into one travel itinerary.

## Features

* Collects complete trip details from the user
* Validates user inputs such as:

  * Starting location
  * Destination
  * Travel dates
  * Number of travelers
  * Budget
  * Travel style
  * Interests
* Converts destination names into geographical coordinates
* Fetches current destination weather information
* Calculates route distance and estimated travel duration
* Finds nearby sightseeing places using Geoapify
* Filters sightseeing places according to user interests
* Finds food places and shopping locations
* Generates a multi-day travel itinerary
* Supports different travel styles:

  * Budget
  * Normal
  * Luxury
* Estimates transportation, accommodation, food, activities, and emergency expenses
* Selects accommodation according to the selected travel style
* Displays remaining budget and budget usage percentage
* Exports the generated travel plan to a JSON file

## Project Workflow

```text
User Input
    ↓
Input Validation
    ↓
Destination Geocoding
    ↓
Weather Information
    ↓
Route Calculation
    ↓
Transportation Estimation
    ↓
Accommodation Selection
    ↓
Places, Food and Shopping Search
    ↓
Interest-Based Filtering
    ↓
Budget Calculation
    ↓
Itinerary Generation
    ↓
JSON Export
```

## Technologies Used

* Python
* Requests
* Geoapify Places API
* Geocoding API
* Weather API
* OpenStreetMap-based routing services
* python-dotenv
* JSON
* Object-oriented and modular Python programming concepts

## Project Structure

```text
AI Travel Planner/
│
├── app.py
├── main.py
├── planner.py
├── budget.py
├── destination.py
├── destination_services.py
├── geocoding_api.py
├── weather_api.py
├── routing.py
├── transportation.py
├── accommodation.py
├── places.py
├── itinerary.py
├── interest_filter.py
├── shopping.py
├── exporter.py
├── requirements.txt
├── .env
├── trip_plan.json
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rishit0105/Ai-Travel-Planner.git
```

### 2. Open the project folder

```bash
cd Ai-Travel-Planner
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## API Configuration

Create a `.env` file in the root project directory.

Add your Geoapify API key:

```env
GEOAPIFY_API_KEY=your_geoapify_api_key
```

Do not upload your `.env` file or API keys to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

## Running the Project

Run the application using:

```bash
python main.py
```

If your project uses `app.py` as the main entry point, run:

```bash
python app.py
```

Follow the prompts to enter:

1. Starting location
2. Destination
3. Start date
4. End date
5. Number of travelers
6. Budget
7. Travel style
8. Interests

## Example Input

```text
Starting location: Delhi
Destination: Jaipur
Start date: 20/09/2026
End date: 23/09/2026
Number of travelers: 2
Budget: 800000
Interests: nature, food, adventure, culture, shopping
Travel style: luxury
```

## Example Output

The application generates:

* Destination information
* Weather details
* Route distance and duration
* Transportation estimate
* Accommodation selection
* Sightseeing recommendations
* Food recommendations
* Shopping recommendations
* Day-wise itinerary
* Budget breakdown
* Remaining budget
* Budget status

The generated plan is saved as:

```text
trip_plan.json
```

## Budget Categories

The current budget estimation divides expenses into the following categories:

| Category       | Allocation |
| -------------- | ---------: |
| Transportation |        30% |
| Accommodation  |        30% |
| Food           |        20% |
| Activities     |        10% |
| Emergency      |        10% |

The application also reports:

* Estimated total cost
* Remaining budget
* Budget status
* Budget usage percentage
* Highest expense category

## Current Limitations

The current version is a functional prototype. Some components still use estimated or mock data:

* Transportation options are currently sample estimates
* Accommodation options are currently sample hotel categories
* Food and shopping results depend on API availability
* Itinerary distribution is currently based mainly on the number of places
* Travel costs may not reflect real-time prices
* The application currently runs through a Python interface

## Future Improvements

* Integrate real-time transportation APIs
* Integrate real hotel and accommodation APIs
* Add live flight, train, and bus prices
* Add a graphical web interface
* Add an interactive map
* Add user login and saved trips
* Add weather forecasts for the complete travel period
* Improve itinerary generation using geographical clustering
* Add hotel ratings and reviews
* Add estimated travel time between sightseeing locations
* Add AI-generated personalized travel suggestions
* Add PDF itinerary export
* Deploy the application as a web app

## Learning Outcomes

This project demonstrates practical experience with:

* Python programming
* Modular project architecture
* API integration
* Environment variable management
* Input validation
* JSON data handling
* Budget optimization logic
* Data filtering
* Itinerary generation
* Error handling
* Working with geographical data
* Building an end-to-end software prototype

## Project Status

**Current status:** Working MVP

The core travel-planning workflow has been implemented and tested successfully. The next development stage is integrating real transportation and accommodation data, followed by a web interface.

## Author

**Rishit Goyal**

GitHub: [Rishit0105](https://github.com/Rishit0105)

Repository: [AI Travel Planner](https://github.com/Rishit0105/Ai-Travel-Planner)
