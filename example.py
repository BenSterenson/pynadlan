import asyncio
from pynadlan.api import get_avg_prices, get_rent_prices


async def main():
    query = "רמת גן"

    sell_latest = await get_avg_prices(query)
    print("Sell latest:", sell_latest)

    rent_latest = await get_rent_prices(query)
    print("Rent latest:", rent_latest)

    # Example requesting specific rooms
    sell_3_4 = await get_avg_prices(query, rooms=[3, 4])
    print("Sell 3-4 rooms:", sell_3_4)

    rent_2 = await get_rent_prices(query, rooms=2)
    print("Rent 2 rooms:", rent_2)


if __name__ == "__main__":
    asyncio.run(main())
