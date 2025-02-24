import asyncio
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv
from tqdm import tqdm

from utils.art_ids import parse_art_id

load_dotenv()

# async def main():
#     collected_image_ids = set()
#     collected_illustration_ids = set()
#
#     async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
#         all_ids = await pool.fetch("SELECT card.id as card_id, image.scryfall_url as image_url, illustration.scryfall_url as illustration_url, illustration.id as old_illustration_id FROM card join image on card.image_id = image.id join illustration on card.illustration_id = illustration.id")
#
#         for card in tqdm(all_ids):
#             card_id = card["card_id"]
#             image_url = card["image_url"]
#             illustration_url = card["illustration_url"]
#             old_illustration_id = card["old_illustration_id"]
#
#             image_id = parse_art_id(image_url)
#             illustration_id = parse_art_id(illustration_url)
#
#             collected_image_ids.add(image_id)
#             collected_illustration_ids.add(illustration_id)
#
#             image_path = Path(f"../mtg_cards/images/{card_id}.png")
#             if image_path.exists():
#                 try:
#                     image_path.rename(f"../mtg_cards/fixed_images/{image_id}.png")
#                 except FileExistsError:
#                     pass
#
#             illustration_path = Path(f"../mtg_cards/illustrations/{old_illustration_id}.png")
#             if illustration_path.exists():
#                 try:
#                     illustration_path.rename(f"../mtg_cards/fixed_illustrations/{illustration_id}.png")
#                 except FileExistsError:
#                     pass


async def main():
    path = Path("../mtg_cards/fixed_images/5140d5d0-15ad-45b2-8ae8-aa53b1cd8132.png")
    print(path.exists())




if __name__ == "__main__":
    asyncio.run(main())