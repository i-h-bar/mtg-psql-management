import asyncio

import asyncpg
from asyncpg import Pool


async def delete_indexes(pool: Pool) -> None:
    try:
        await asyncio.gather(
            pool.execute("drop index rule_multi_index"),
            pool.execute("drop index card_index_id_name_date_rule_id"),
            return_exceptions=False
        )
    except asyncpg.exceptions.UndefinedObjectError:
        pass

async def add_indexes(pool: Pool) -> None:
    rule_index = """    
                create index rule_multi_index
                    on rule (
                             id,
                             mana_cost,
                             power,
                             toughness,
                             loyalty,
                             defence,
                             type_line,
                             keywords,
                             oracle_text
                        );
    """

    card_index = """
                create index card_index_id_name_date_rule_id
                    on card(id, name, normalised_name, release_date, rule_id);
            """

    await asyncio.gather(
        pool.execute(rule_index),
        pool.execute(card_index),
        return_exceptions=False
    )
