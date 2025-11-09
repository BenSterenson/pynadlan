import asyncio
from pynadlan.api import get_autocomplete_lists, get_cities_summary, get_neighborhoods_summary, get_city_timeseries, get_street_deals


async def main():
    # Autocomplete lists (static)
    lists = get_autocomplete_lists()
    print("First 5 cities:", lists["cities"][:5])
    print("First 5 cities+neighborhoods:", lists["cities_and_neighborhoods"][:5])

    # Cities summary - get median prices across all cities
    print("\n--- Cities Summary ---")
    summary = await get_cities_summary(min_deals=100)
    print(f"Total cities: {summary['total_cities']}")
    print(f"Total deals: {summary['total_deals_all_cities']}")
    print(f"Top 5 cities by deal volume:")
    for city in summary['cities'][:5]:
        print(f"  {city['city_name']}: {city['total_deals']} deals, median price: ₪{city['medianPrice']:,}")

    # Neighborhoods summary - get neighborhood breakdown for a specific city
    print("\n--- Neighborhoods Summary for תל אביב יפו ---")
    neighborhoods = await get_neighborhoods_summary(city="תל אביב יפו", min_deals=10)
    print(f"Average median price: ₪{neighborhoods['average_median_price_overall']:,.0f}")
    print(f"Total neighborhoods: {len(neighborhoods['neighborhoods'])}")
    print(f"Top 5 neighborhoods by deal volume:")
    for neighborhood in neighborhoods['neighborhoods'][:5]:
        print(f"  {neighborhood['neighborhood']}: {neighborhood['total_deals']} deals, median price: ₪{neighborhood['median_price']:,}")

    # City timeseries - get historical price trends
    print("\n--- City Timeseries for תל אביב יפו (1 year) ---")
    timeseries = await get_city_timeseries(city="תל אביב יפו", property_type="apartment", time_range="1year")
    print(f"Total data points: {timeseries['metadata']['totalDataPoints']}")
    print(f"Room categories: {timeseries['metadata']['totalRoomCategories']}")
    print("\nSummary by room count:")
    for room_category, stats in timeseries['summaries'].items():
        print(f"  {room_category}:")
        print(f"    Latest price: ₪{stats['latestPrice']:,} ({stats['latestMonth']} {stats['latestYear']})")
        print(f"    Avg price: ₪{stats['avgPrice']:,.0f}")
        print(f"    Total transactions: {stats['totalTransactions']}")

    # Street deals - get detailed transaction data for a specific street
    print("\n--- Street Deals for תל אביב יפו_גורדון---")
    street_deals = await get_street_deals(city_street="תל אביב יפו_גורדון", per_page=100)
    print(f"Street: {street_deals['street']} in {street_deals['city']}")
    print(f"Total deals: {street_deals['summary']['totalDeals']}")
    print(f"Median price: ₪{street_deals['summary']['medianPrice']:,}")
    print(f"Average price: ₪{street_deals['summary']['avgPrice']:,.0f}")
    print(f"Date range: {street_deals['summary']['dateRange']}")
    print(f"\nFirst 5 deals:")
    for deal in street_deals['deals'][:5]:
        sqm = f", {deal['squareMeters']}m²" if deal.get('squareMeters') else ""
        print(f"  {deal['rooms']} rooms, floor {deal['floor']}{sqm} - ₪{deal['price']:,} ({deal['saleDate']})")


if __name__ == "__main__":
    asyncio.run(main())
