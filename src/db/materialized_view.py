import contextlib
import logging

from asyncpg import OutOfMemoryError, Pool
from asyncpg.exceptions import DuplicateTableError
from tqdm import tqdm

from db.queries.materialised_views import artists, distinct_card, sets
from db.queries.materialised_views.drop_all import DROP_MAT_VIEWS

logger = logging.getLogger(__name__)


async def create_mv_distinct(pool: Pool) -> None:
    await pool.execute(distinct_card.CREATE)


async def create_mv_for_set(set_: str, pool: Pool, pbar: tqdm) -> None:
    with contextlib.suppress(DuplicateTableError):
        await pool.execute(sets.CREATE.format(set=set_.replace(" ", "_"), normalised_name=set_))

    pbar.update()


async def create_mv_for_artist(artist: str, pool: Pool, pbar: tqdm) -> None:
    with contextlib.suppress(DuplicateTableError):
        await pool.execute(artists.CREATE.format(artist=artist.replace(" ", "_"), normalised_name=artist))

    pbar.update()


async def drop_all_mv(pool: Pool) -> None:
    logger.info("Dropping all materialised views...")
    try:
        await pool.execute(DROP_MAT_VIEWS)
    except OutOfMemoryError:
        await slow_drop_all_mv(pool)


async def slow_drop_all_mv(pool: Pool) -> None:
    mvs = await pool.fetchval(
        """SELECT array_agg(oid::regclass::text)
            FROM   pg_class
            WHERE  relkind = 'm';"""
    )
    if mvs is not None:
        with tqdm(total=len(mvs)) as pbar:
            pbar.set_description("Drop all MVs")
            pbar.refresh()
            for mv in mvs:
                await pool.execute(f"DROP MATERIALIZED VIEW {mv};")
                pbar.update()
