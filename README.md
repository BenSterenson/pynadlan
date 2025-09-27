# pynadlan

Lightweight async helpers to fetch Israeli real-estate histogram data by city/neighborhood and extract the latest sell/rent prices per room count.

### Installation

```bash
pip install -e .
```

### Quickstart

```python
import asyncio
from pynadlan.api import get_avg_prices, get_rent_prices

async def main():
    query = "רמת גן"  # city or neighborhood

    sell_latest = await get_avg_prices(query)
    # => {"sell_2_price": 2500000, "sell_3_price": 3200000, ...}
    print(sell_latest)

    rent_latest = await get_rent_prices(query)
    # => {"rent_2_price": 6500, "rent_3_price": 7500, ...}
    print(rent_latest)

    # Filter by specific room counts
    print(await get_avg_prices(query, rooms=[3, 4]))
    print(await get_rent_prices(query, rooms=2))

if __name__ == "__main__":
    asyncio.run(main())
```

### API

- `get_avg_prices(query: str, rooms: int | list[int] | None = None) -> dict`
  - Returns the latest sell prices keyed by `sell_{rooms}_price`.
  - If `rooms` is omitted, returns all available room-based series from the endpoint.
  - If `rooms` is provided but some series are missing in the payload, they are returned as `None`.

- `get_rent_prices(query: str, rooms: int | list[int] | None = None) -> dict`
  - Returns the latest rent prices keyed by `rent_{rooms}_price`.
  - Same filtering behavior as `get_avg_prices`.

### Notes

- The functions are async and should be awaited.
- Input `query` is URL-encoded automatically.
- Output values are the last value from each histogram series.