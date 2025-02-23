import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

import aiofiles
import aiohttp
from dotenv import load_dotenv

load_dotenv()


file_regex = re.compile(r"default-cards-(\d+)\.json")


def look_for_data_file() -> str | None:
    for file in Path().iterdir():
        if match := file_regex.match(file.name):
            date = datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
            if date < (datetime.now() - timedelta(days=6, hours=23)):
                print(f"Deleting stale card data: {file.name}")
                file.unlink()
            else:
                return file


async def load_data_file(data_file: str | Path) -> list[dict]:
    async with aiofiles.open(data_file, encoding="utf-8") as file:
        return json.loads(await file.read())


async def download_scryfall_data() -> list[dict] | None:
    print("Downloading from Scryfall")
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://api.scryfall.com/bulk-data")
        bulk_data_info = await response.json()

        for category in bulk_data_info["data"]:
            if category["type"] == "default_cards":
                response = await session.get(category["download_uri"])
                data = await response.json()

                async with aiofiles.open(
                        f"default-cards-{datetime.now().strftime("%Y%m%d%H%M%S")}.json", "w", encoding="utf-8"
                ) as file:
                    await file.write(json.dumps(data))

                return data


async def load_scryfall_data() -> list[dict] | None:
    if data_file := os.getenv("FILE"):
        print("Found file specified by environment variables.")
        return await load_data_file(data_file)

    if data_file := look_for_data_file():
        print("Found cached data from previous download less than a week old.")
        return await load_data_file(data_file)

    return await download_scryfall_data()
