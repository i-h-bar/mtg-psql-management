import asyncio

import asyncpg
from asyncpg import Pool
from tqdm import tqdm

from db.queries import INSERT_RELATED_TOKEN, INSERT_COMBO
from models.combos import Combo
from models.related_tokens import RelatedToken
from models.post_inserts import token_relations, combo_relations


async def insert_relation(related_token: RelatedToken, pbar: tqdm, pool: Pool) -> None:
    try:
        await pool.execute(INSERT_RELATED_TOKEN, related_token.id, related_token.card_id, related_token.token_id)
    except asyncpg.exceptions.ForeignKeyViolationError:
        pass

    pbar.update()

async def insert_token_relations(pool: Pool) -> None:
    with tqdm(total=len(token_relations)) as pbar:
        pbar.set_description("Inserting token relations")
        pbar.refresh()
        await asyncio.gather(*(insert_relation(related_token, pbar, pool) for related_token in token_relations))


async def insert_combo(combo: Combo, pbar: tqdm, pool: Pool) -> None:
    try:
        await pool.execute(INSERT_COMBO, combo.id, combo.card_id, combo.combo_card_id)
    except asyncpg.exceptions.ForeignKeyViolationError:
        pass

    pbar.update()

async def insert_combos(pool: Pool) -> None:
    with tqdm(total=len(combo_relations)) as pbar:
        pbar.set_description("Inserting combos")
        pbar.refresh()
        await asyncio.gather(*(insert_combo(combo, pbar, pool) for combo in combo_relations))