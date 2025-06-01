import asyncio
import contextlib

from asyncpg import Pool
from asyncpg.exceptions import ForeignKeyViolationError
from tqdm import tqdm

from src.db.queries import INSERT_COMBO, INSERT_RELATED_TOKEN
from src.models.combos import Combo
from src.models.post_inserts import combo_relations, token_relations
from src.models.related_tokens import RelatedToken


async def insert_relation(related_token: RelatedToken, pbar: tqdm, pool: Pool) -> None:
    with contextlib.suppress(ForeignKeyViolationError):
        await pool.execute(
            INSERT_RELATED_TOKEN,
            related_token.id,
            related_token.card_id,
            related_token.token_id,
        )

    pbar.update()


async def insert_token_relations(pool: Pool) -> None:
    with tqdm(total=len(token_relations)) as pbar:
        pbar.set_description("Inserting token relations")
        pbar.refresh()
        await asyncio.gather(*(insert_relation(related_token, pbar, pool) for related_token in token_relations))


async def insert_combo(combo: Combo, pbar: tqdm, pool: Pool) -> None:
    with contextlib.suppress(ForeignKeyViolationError):
        await pool.execute(INSERT_COMBO, combo.id, combo.card_id, combo.combo_card_id)

    pbar.update()


async def insert_combos(pool: Pool) -> None:
    with tqdm(total=len(combo_relations)) as pbar:
        pbar.set_description("Inserting combos")
        pbar.refresh()
        await asyncio.gather(*(insert_combo(combo, pbar, pool) for combo in combo_relations))
