import asyncpg

from asyncpg import Pool
from tqdm import tqdm

from db.queries import CREATE_SET_MV, CREATE_ARTIST_MV


async def create_mv_distinct(pool: Pool):
    await pool.execute(
        """
        create materialized view distinct_cards as
            select distinct on (front.name) front.id                    as front_id,
                                            front.name                  as front_name,
                                            front.normalised_name       as front_normalised_name,
                                            front_image.png             as front_png,
                                            front_image.scryfall_url    as front_scryfall_url,
                                            back.id                     as back_id,
                                            back.name                   as back_name,
                                            back_image.scryfall_url     as back_scryfall_url,
                                            back_image.png              as back_png,
                                            front.release_date          as release_date
            from card front
                     left join card back on front.backside_id = back.id
                     left join image front_image on front.image_id = front_image.id
                     left join image back_image on back.image_id = back_image.id
            order by front.name, front.release_date desc;
        """
    )


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

async def drop_all_mv(pool: Pool) -> None:
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