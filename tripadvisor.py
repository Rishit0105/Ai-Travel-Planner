import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotels"

headers = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": "tripadvisor16.p.rapidapi.com"
}

params = {
    "geoId": "293919",       # example Goa geoId — we'll verify this
    "checkIn": "2026-10-20",
    "checkOut": "2026-10-23",
    "pageNumber": "1",
    "currencyCode": "INR"
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

print("Status:", response.status_code)
print(response.json())