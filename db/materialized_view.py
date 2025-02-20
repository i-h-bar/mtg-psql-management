import asyncpg

from asyncpg import Pool
from tqdm import tqdm

from db.queries import CREATE_SET_MV, CREATE_ARTIST_MV


async def create_mv_for_set(set_: str, pool: Pool, pbar: tqdm) -> None:
    try:
        await pool.execute(CREATE_SET_MV.format(set=set_.replace(" ", "_"), normalised_name=set_))
    except asyncpg.exceptions.DuplicateTableError:
        pass

    pbar.update()


async def create_mv_for_artist(artist: str, pool: Pool, pbar: tqdm) -> None:
    try:
        await pool.execute(CREATE_ARTIST_MV.format(artist=artist.replace(" ", "_"), normalised_name=artist))
    except asyncpg.exceptions.DuplicateTableError:
        pass

    pbar.update()
