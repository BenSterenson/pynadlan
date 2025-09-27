# Dirobot Histogram Integration

Replace legacy GovMap API usage with dirobot histogram endpoint and expose helpers.

## Completed Tasks

- [x] Add dirobot fetch and parsing functions to `pynadlan/api.py`
- [x] Return latest sell prices per room via `get_avg_prices`
- [x] Return latest rent prices per room via `get_rent_prices`
- [x] Update `example.py` to demonstrate new functions

## In Progress Tasks

- [ ] Create/update this task list with relevant files and details

## Future Tasks

- [ ] Add retries and backoff for network errors
- [ ] Validate query and normalize room inputs (2-6 bounds)
- [ ] Publish a minor version in `setup.py`

## Implementation Plan

We call `https://dirobot.co.il/api/analysis/histograms/{query}` where `query` is a city/neighborhood. We parse `real_estate_histograms` and extract the last value from each `*_price` series for sell/rent.

### Relevant Files

- `pynadlan/api.py` – New helpers: `get_avg_prices`, `get_rent_prices`; internal fetch/parsers
- `example.py` – Usage example invoking both helpers