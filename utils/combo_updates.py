import asyncio

from asyncpg import Pool
from tqdm import tqdm

from db.post_bulk_inserts import insert_combo
from models.combos import Combo


async def update_combos(data: tuple[dict, ...], pool: Pool) -> None:
    current_combos = {
        (str(record["card_id"]), str(record["combo_card_id"]))
        for record in await pool.fetch("select card_id, combo_card_id from combo")
    }

    missing_combos = []
    for card in data:
        if parts := card.get("all_parts"):
            for part in parts:
                if part["component"] == "combo_piece":
                    card_id, combo_card_id = card["id"], part["id"]
                    if (card_id, combo_card_id) not in current_combos:
                        missing_combos.append(
                            Combo(card_id=card_id, combo_card_id=combo_card_id)
                        )

    with tqdm(total=len(missing_combos)) as pbar:
        pbar.set_description("Adding missing combos")
        pbar.refresh()
        await asyncio.gather(
            *(insert_combo(combo, pbar, pool) for combo in missing_combos)
        )
