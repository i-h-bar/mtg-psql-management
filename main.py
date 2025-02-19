import asyncio
import json
import os

import aiofiles
from dotenv import load_dotenv

from db.insert import insert_card

load_dotenv()


async def main():
    async with aiofiles.open(os.getenv("FILE"), encoding="utf-8") as file:
        data = json.loads(await file.read())

    await asyncio.gather(*(insert_card(card) for card in data))



if __name__ == '__main__':
    asyncio.run(main())