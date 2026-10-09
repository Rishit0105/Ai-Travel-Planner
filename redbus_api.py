from redbus_final_scraper import RedBusHybridScraper

scraper = RedBusHybridScraper()

# Search any route
buses = scraper.search_buses("Delhi", "Jaipur", "2026-09-23")

# Use the live data
for bus in buses:
    print(f"{bus['operator']}: {bus['price']}")

scraper.close()