import asyncio

import aiofiles
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        result = await session.get("https://cards.scryfall.io/png/front/0/0/008df307-f010-47bc-8548-65a1c7b1c4b8.png?1559601144")
        png = await result.read()

        async with aiofiles.open("folder/poc.png", "wb") as f:
            await f.write(png)


if __name__ == '__main__':
    asyncio.run(main())