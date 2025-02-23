import asyncpg

from asyncpg import Pool
from tqdm import tqdm

from db.queries import CREATE_SET_MV, CREATE_ARTIST_MV


async def create_mv_distinct(pool: Pool):
    await pool.execute(
        """
            create materialized view distinct_cards as
                select distinct on (front.name) front.id               as front_id,
                                                front.name             as front_name,
                                                front.normalised_name  as front_normalised_name,
                                                front.image_id         as front_image_id,
                                                front_rule.mana_cost   as front_mana_cost,
                                                front_rule.power       as front_power,
                                                front_rule.toughness   as front_toughness,
                                                front_rule.loyalty     as front_loyalty,
                                                front_rule.defence     as front_defence,
                                                front_rule.type_line   as front_type_line,
                                                front_rule.keywords    as front_keywords,
                                                front_rule.oracle_text as front_oracle_text,
                
                                                back.id                as back_id,
                                                back.name              as back_name,
                                                back.image_id          as back_image_id,
                                                back_rule.mana_cost    as back_mana_cost,
                                                back_rule.power        as back_power,
                                                back_rule.toughness    as back_toughness,
                                                back_rule.loyalty      as back_loyalty,
                                                back_rule.defence      as back_defence,
                                                back_rule.type_line    as back_type_line,
                                                back_rule.keywords     as back_keywords,
                                                back_rule.oracle_text  as back_oracle_text,
                
                                                front.release_date     as release_date
                from card front
                         left join card back on front.backside_id = back.id
                         left join rule front_rule on front.rule_id = front_rule.id
                         left join rule back_rule on back.rule_id = back_rule.id
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