import httpx
from typing import Any, Optional, Union
from urllib.parse import quote
from .locations import CITIES, CITIES_AND_NEIGHBORHOODS


async def _fetch_histograms(query: str) -> dict[str, Any]:
    """
    Fetch histogram data from dirobot for a given query (city/neighborhood).

    Returns the parsed JSON payload.
    """
    encoded_query = quote(query, safe="")
    url = f"https://dirobot.co.il/api/analysis/histograms/{encoded_query}"

    # Keep an independent short-lived client for this endpoint
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


def _latest_value(points: list[dict[str, Any]]) -> Optional[Union[int, float]]:
    if not points:
        return None
    # Points are chronological; take the last value
    last_point = points[-1]
    return last_point.get("value")


def _extract_latest_by_prefix(payload: dict[str, Any], prefix: str, rooms: list[int] | None) -> dict[str, Optional[Union[int, float]]]:
    """
    From the histograms payload, extract the latest value for each histogram_type
    that starts with the given prefix (e.g., "sell_" or "rent_").

    If rooms is provided, only include keys for those room counts (e.g., 2..6).
    """
    histograms: list[dict[str, Any]] = payload.get("real_estate_histograms", [])

    latest: dict[str, Optional[Union[int, float]]] = {}

    # Build the set of expected keys when rooms are specified
    expected_keys: Optional[set] = None
    if rooms is not None:
        expected_keys = {f"{prefix}{room}_price" for room in rooms}

    for item in histograms:
        h_type = item.get("histogram_type")
        if not isinstance(h_type, str):
            continue
        if not h_type.startswith(prefix):
            continue

        # Only keep room-specific price series (e.g., sell_2_price) and not aggregated ones
        if not h_type.endswith("_price"):
            continue

        if expected_keys is not None and h_type not in expected_keys:
            continue

        value = _latest_value(item.get("histogram_points", []))
        latest[h_type] = value

    # If rooms were specified but some keys were missing from the payload, include them as None
    if expected_keys is not None:
        for key in expected_keys:
            latest.setdefault(key, None)

    return latest


async def get_avg_prices(query: str, rooms: Optional[Union[int, list[int]]] = None) -> dict[str, Optional[Union[int, float]]]:
    """
    Return latest sell prices per room type for the given query.

    - query: city or neighborhood string (Hebrew/English supported)
    - rooms: optional single room count (e.g., 3) or list of room counts (e.g., [3,4])

    Example return (rooms unspecified):
    {"sell_2_price": 2500000, "sell_3_price": 3200000, ...}
    """
    rooms_list: Optional[list[int]]
    if rooms is None:
        rooms_list = None
    elif isinstance(rooms, int):
        rooms_list = [rooms]
    else:
        rooms_list = list(rooms)

    payload = await _fetch_histograms(query)
    return _extract_latest_by_prefix(payload, prefix="sell_", rooms=rooms_list)


async def get_rent_prices(query: str, rooms: Optional[Union[int, list[int]]] = None) -> dict[str, Optional[Union[int, float]]]:
    """
    Return latest rent prices per room type for the given query.

    - query: city or neighborhood string (Hebrew/English supported)
    - rooms: optional single room count (e.g., 3) or list of room counts (e.g., [3,4])

    Example return (rooms unspecified):
    {"rent_2_price": 6500, "rent_3_price": 7500, ...}
    """
    rooms_list: Optional[list[int]]
    if rooms is None:
        rooms_list = None
    elif isinstance(rooms, int):
        rooms_list = [rooms]
    else:
        rooms_list = list(rooms)

    payload = await _fetch_histograms(query)
    return _extract_latest_by_prefix(payload, prefix="rent_", rooms=rooms_list)


def get_autocomplete_lists() -> dict[str, list[str]]:
    """
    Return static autocomplete lists for cities and for cities+neighborhoods.
    Structure:
    {
        "cities": [...],
        "cities_and_neighborhoods": [...]
    }
    """
    return {
        "cities": list(CITIES),
        "cities_and_neighborhoods": list(CITIES_AND_NEIGHBORHOODS),
    }