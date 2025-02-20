import asyncio

import asyncpg
from asyncpg import Pool
from tqdm import tqdm

from db.queries import INSERT_RELATED_TOKEN
from models.related_tokens import RelatedToken
from models.tokens import token_relations


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
