import asyncio
import json

import aiofiles
import aiohttp

from utils.single_faced import produce_card


async def main():
    async with aiofiles.open("oracle-cards-20250218220727.json", encoding="utf-8") as file:
        data = json.loads(await file.read())


    for card in data:
        if not card.get("card_faces"):
            card_data = produce_card(card)
            x = 0
        else:
            print(card["name"])


if __name__ == '__main__':
    asyncio.run(main())