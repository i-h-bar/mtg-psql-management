import asyncio
import json

import aiofiles


async def main():
    async with aiofiles.open("unique-artwork-20250218100456.json", encoding="utf-8") as file:
        data = json.loads(await file.read())

    x = 0


if __name__ == '__main__':
    asyncio.run(main())