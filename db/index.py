import asyncio

import asyncpg
from asyncpg import Pool


async def delete_indexes(pool: Pool) -> None:
    try:
        await asyncio.gather(
            pool.execute("drop index image_id_png_index"),
            pool.execute("drop index related_card_card_id_related_card_id_index"),
            pool.execute("drop index card_multi_index"),
            return_exceptions=False
        )
    except asyncpg.exceptions.UndefinedObjectError:
        pass

async def add_indexes(pool: Pool) -> None:
    image_index = """    
                create index image_id_png_index
                    on image(id, png);
    """


    related_card_index = """
                create index related_card_card_id_related_card_id_index
                    on related_card(card_id, related_card_id);
                """

    card_index = """
                create index card_multi_index
                    on card(id, name, normalised_name, image_id, release_date);
            """

    await asyncio.gather(
        pool.execute(image_index),
        pool.execute(related_card_index),
        pool.execute(card_index),
        return_exceptions=False
    )
