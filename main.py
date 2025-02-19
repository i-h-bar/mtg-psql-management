import asyncio
import json

import aiofiles

from utils.dual_faced import produce_dual_faced_card
from utils.single_faced import produce_card


async def main():
    async with aiofiles.open("oracle-cards-20250218220727.json", encoding="utf-8") as file:
        data = json.loads(await file.read())

    for card in data:
        if card.get("set_type") == "memorabilia":
            continue

        if not (sides := card.get("card_faces")):
            card_data = produce_card(card)
        else:
            front, back = produce_dual_faced_card(card, sides[0], sides[1])


if __name__ == '__main__':
    asyncio.run(main())