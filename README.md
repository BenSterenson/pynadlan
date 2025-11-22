# pynadlan

Lightweight async helpers to fetch Israeli real-estate data including historical price trends, city/neighborhood statistics, and detailed transaction records from the dirobot.co.il API.

### Installation

```bash
pip install -e .
```

### Quickstart

```python
import asyncio
from pynadlan.api import (
    get_avg_prices,
    get_rent_prices,
    get_cities_summary,
    get_neighborhoods_summary,
    get_city_timeseries,
    get_street_deals,
    get_locations_search,
    get_autocomplete_lists
)

async def main():
    # Location search - dynamic autocomplete with market data
    search = await get_locations_search("רות", per_page=5)
    # => {"results": [...], "pagination": {...}, "summary": {...}}

    # Use search results to fetch detailed data
    location = search["results"][0]
    if location["type"] == "street":
        city_street = f"{location['city']}_{location['street']}"
        deals = await get_street_deals(city_street)
    elif location["type"] in ["neighborhood", "city"]:
        prices = await get_avg_prices(location["display_name"])

    # Historical price queries (histogram data)
    query = "רמת גן"
    sell_latest = await get_avg_prices(query)
    # => {"sell_2_price": 2500000, "sell_3_price": 3200000, ...}

    rent_latest = await get_rent_prices(query, rooms=[3, 4])
    # => {"rent_3_price": 7500, "rent_4_price": 9000}

    # Cities summary - median prices across all Israeli cities
    summary = await get_cities_summary(min_deals=100)
    # => {"total_cities": 303, "cities": [...], "total_deals_all_cities": 88081, ...}

    # Neighborhoods summary - breakdown for a specific city
    neighborhoods = await get_neighborhoods_summary(city="תל אביב יפו", min_deals=10)
    # => {"neighborhoods": [...], "average_median_price_overall": 2600725.6, ...}

    # City timeseries - historical price trends over time
    timeseries = await get_city_timeseries(city="תל אביב יפו", time_range="1year")
    # => {"timeSeriesByRooms": {...}, "summaries": {...}, "metadata": {...}}

    # Street deals - detailed transaction data for a specific street
    deals = await get_street_deals(city_street="תל אביב יפו_גורדון", per_page=100)
    # => {"deals": [...], "summary": {"medianPrice": ..., "totalDeals": ...}, ...}

    # Static autocomplete lists
    lists = get_autocomplete_lists()
    # => {"cities": [...], "cities_and_neighborhoods": [...]}

if __name__ == "__main__":
    asyncio.run(main())
```

### API Reference

#### Location Search

**`get_locations_search(query: str, page: int = 1, per_page: int = 20, min_deals: int | None = None, location_type: str = "all") -> dict`**
- Search for locations (cities, neighborhoods, streets) matching a query string
- Provides dynamic autocomplete with real-time market data
- `query`: Search string in Hebrew or English
- `page`: Page number for pagination (default: 1)
- `per_page`: Results per page (default: 20)
- `min_deals`: Optional minimum number of deals to filter results
- `location_type`: Filter by type - `"all"`, `"city"`, `"neighborhood"`, `"street"` (default: `"all"`)
- Returns: `results` array with location details, `pagination` info, `summary` statistics
- Each result includes: `type`, `name`, `display_name`, `city`, `neighborhood`/`street`, `median_price`, `total_deals`, `date_range`

**Recommended workflow:**
```python
# Search for locations
results = await get_locations_search("רות")

# Get detailed data based on location type
location = results["results"][0]
if location["type"] == "street":
    deals = await get_street_deals(f"{location['city']}_{location['street']}")
elif location["type"] in ["neighborhood", "city"]:
    prices = await get_avg_prices(location["display_name"])
```

#### Historical Price Data (Histogram-based)

**`get_avg_prices(query: str, rooms: int | list[int] | None = None) -> dict`**
- Returns the latest sell prices per room count for a city/neighborhood
- Keyed by `sell_{rooms}_price` (e.g., `sell_3_price`, `sell_4_price`)
- If `rooms` is omitted, returns all available room-based series
- If `rooms` is provided but some series are missing, they are returned as `None`

**`get_rent_prices(query: str, rooms: int | list[int] | None = None) -> dict`**
- Returns the latest rent prices per room count for a city/neighborhood
- Keyed by `rent_{rooms}_price` (e.g., `rent_3_price`, `rent_4_price`)
- Same filtering behavior as `get_avg_prices`

#### Aggregate Statistics

**`get_cities_summary(min_deals: int = 10) -> dict`**
- Returns median prices and deal counts across all Israeli cities
- Results include: `total_cities`, `total_deals_all_cities`, `cities` array
- Each city includes: `city_name`, `medianPrice`, `total_deals`, `date_range`
- Sorted by deal volume (most active cities first)

**`get_neighborhoods_summary(city: str, min_deals: int = 3) -> dict`**
- Returns neighborhood-level statistics for a specific city
- City name should be in Hebrew (e.g., "תל אביב יפו", "רעננה")
- Results include: `neighborhoods` array, `average_median_price_overall`
- Each neighborhood includes: `neighborhood`, `median_price`, `total_deals`, `unique_streets`

#### Historical Trends

**`get_city_timeseries(city: str, property_type: str = "apartment", time_range: str = "1year") -> dict`**
- Returns historical price trends over time for a city, broken down by room count
- `time_range` options: `"1year"`, `"2years"`, `"all"`
- Results include monthly data: `marketValue`, `askingPrice`, `growth`, `transactionCount`
- Summary statistics per room category: `avgPrice`, `minPrice`, `maxPrice`, `totalTransactions`

#### Detailed Transaction Data

**`get_street_deals(city_street: str, per_page: int = 10000) -> dict`**
- Returns detailed transaction/deal data for a specific street
- `city_street` format: `"city_street"` in Hebrew (e.g., `"תל אביב יפו_גורדון"`)
- Results include individual deals with: `buildYear`, `floor`, `price`, `rooms`, `saleDate`, `squareMeters` (optional)
- Summary statistics: `avgPrice`, `medianPrice`, `totalDeals`, `avgPricePerSquareMeter`
- Includes pagination information

#### Utilities

**`get_autocomplete_lists() -> dict`** (synchronous)
- Returns static lists for autocomplete functionality
- Keys: `cities` (array of city names), `cities_and_neighborhoods` (combined array)

### Notes

- All data-fetching functions are async and must be awaited
- Query parameters (city/neighborhood names) are URL-encoded automatically
- Hebrew and English city names are supported where applicable
- All prices are in ILS (Israeli Shekels)