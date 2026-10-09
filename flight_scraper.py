"""
Flight search scraper - uses Selenium to extract flight data from Google Flights
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import json
import re


class FlightScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        self.driver = webdriver.Chrome(options=chrome_options)

    def search_flights(self, source, destination, date, return_date=None):
        """
        Search flights - supports one-way and round-trip
        """
        try:
            # Build Google Flights URL
            trip_type = "2" if return_date else "1"  # 1=one-way, 2=round-trip

            url = f"https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{source}%20on%20{date}"
            if return_date:
                url += f"%20through%20{return_date}"

            print(f"Loading: {url}")
            self.driver.get(url)

            # Wait for flights to load
            print("Waiting for flight results...")
            time.sleep(8)

            # Scroll to load more flights
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(1)

            # Try API extraction first
            flights = self._extract_from_api()

            if not flights:
                print("API extraction failed, trying DOM parsing...")
                flights = self._extract_from_dom()

            return flights

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _extract_from_api(self):
        """Extract flight data from network API calls"""
        flights = []

        logs = self.driver.get_log('performance')

        for entry in logs:
            try:
                log = json.loads(entry['message'])['message']

                if log['method'] == 'Network.responseReceived':
                    response = log['params']['response']
                    url = response['url']

                    if 'flights' in url.lower() or 'shopping' in url.lower():
                        request_id = log['params']['requestId']

                        try:
                            response_body = self.driver.execute_cdp_cmd(
                                'Network.getResponseBody',
                                {'requestId': request_id}
                            )

                            body = response_body.get('body', '')
                            if body:
                                data = json.loads(body)

                                with open('flight_api_response.json', 'w', encoding='utf-8') as f:
                                    json.dump(data, f, indent=2)

                                flights = self._parse_api_response(data)
                                if flights:
                                    return flights

                        except:
                            continue
            except:
                continue

        return []

    def _extract_from_dom(self):
        """Extract flight data from page DOM"""
        flights = []

        try:
            # Wait for flight cards
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[class*='pIav']")))

            flight_elements = self.driver.find_elements(By.CSS_SELECTOR, "li[class*='pIav']")
            print(f"Found {len(flight_elements)} flight elements")

            for idx, elem in enumerate(flight_elements[:20]):
                try:
                    flight = self._parse_flight_element(elem, idx)
                    if flight:
                        flights.append(flight)
                except Exception as e:
                    print(f"Error parsing flight {idx}: {e}")
                    continue

        except Exception as e:
            print(f"DOM extraction error: {e}")

        return flights

    def _parse_flight_element(self, elem, idx):
        """Parse individual flight card from DOM"""
        try:
            # Airline name
            airline_elem = elem.find_elements(By.CSS_SELECTOR, "div[class*='sSHqwe']")
            airline = airline_elem[0].text if airline_elem else "Unknown"

            # Times (departure and arrival)
            time_elems = elem.find_elements(By.CSS_SELECTOR, "span[class*='mv1WYe']")
            departure = time_elems[0].text if len(time_elems) > 0 else ""
            arrival = time_elems[1].text if len(time_elems) > 1 else ""

            # Duration
            duration_elem = elem.find_elements(By.CSS_SELECTOR, "div[class*='Ak5kof']")
            duration = duration_elem[0].text if duration_elem else ""

            # Stops
            stops_elem = elem.find_elements(By.CSS_SELECTOR, "div[class*='BbR8Ec']")
            stops = stops_elem[0].text if stops_elem else "Nonstop"

            # Price
            price_elem = elem.find_elements(By.CSS_SELECTOR, "div[class*='YMlIz FpEdX']")
            price = price_elem[0].text if price_elem else "N/A"

            # Flight number/details
            details_elem = elem.find_elements(By.CSS_SELECTOR, "span[class*='EfT7Ae']")
            details = details_elem[0].text if details_elem else ""

            return {
                'airline': airline,
                'flight_number': details,
                'departure': departure,
                'arrival': arrival,
                'duration': duration,
                'stops': stops,
                'price': price
            }

        except Exception as e:
            print(f"Parse error for element {idx}: {e}")
            return None

    def _parse_api_response(self, data):
        """Parse API response for flight data"""
        flights = []

        # Try common API structures
        checks = [
            lambda: data.get('flights', []),
            lambda: data.get('data', {}).get('flights', []),
            lambda: data.get('results', []),
            lambda: data.get('itineraries', []),
        ]

        for getter in checks:
            try:
                flight_list = getter()
                if isinstance(flight_list, list) and len(flight_list) > 0:
                    for f in flight_list:
                        parsed = self._parse_flight_object(f)
                        if parsed:
                            flights.append(parsed)

                    if flights:
                        return flights
            except:
                continue

        return flights

    def _parse_flight_object(self, flight):
        """Parse flight object from API"""
        try:
            return {
                'airline': flight.get('airline', 'Unknown'),
                'flight_number': flight.get('flightNumber', ''),
                'departure': flight.get('departureTime', ''),
                'arrival': flight.get('arrivalTime', ''),
                'duration': flight.get('duration', ''),
                'stops': flight.get('stops', 'Nonstop'),
                'price': flight.get('price', 'N/A')
            }
        except:
            return None

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    scraper = FlightScraper()

    try:
        flights = scraper.search_flights(
            source="DEL",
            destination="BOM",
            date="2026-10-15"
        )

        if flights:
            print(f"\n{'='*70}")
            print(f"✓ Found {len(flights)} flights")
            print('='*70)
            print()

            for i, flight in enumerate(flights, 1):
                print(f"{i}. {flight['airline']} {flight['flight_number']}")
                print(f"   {flight['departure']} → {flight['arrival']} ({flight['duration']})")
                print(f"   {flight['stops']} | Price: {flight['price']}")
                print()

            with open('flights_result.json', 'w', encoding='utf-8') as f:
                json.dump(flights, f, indent=2)
            print("✓ Saved to flights_result.json")
        else:
            print("\n✗ No flights found")

    finally:
        scraper.close()
