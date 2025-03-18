import asyncio

import asyncpg
from asyncpg import Pool


async def delete_indexes(pool: Pool) -> None:
    print("Deleting indexes...")
    try:
        await asyncio.gather(
            pool.execute("drop index rule_multi_index"),
            pool.execute("drop index card_index_id_name_date_rule_id"),
            pool.execute("drop index distinct_cards_ix"),
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

    distinct_cards_ix = """
                create index distinct_cards_ix
                    on distinct_cards(front_name,
                                    front_normalised_name,
                                    front_scryfall_url,
                                    front_image_id,
                                    front_mana_cost,
                                    front_colour_identity,
                                    front_power,
                                    front_toughness,
                                    front_loyalty,
                                    front_defence,
                                    front_type_line,
                                    front_oracle_text,
                                    back_name,
                                    back_scryfall_url,
                                    back_image_id,
                                    back_mana_cost,
                                    back_colour_identity,
                                    back_power,
                                    back_toughness,
                                    back_loyalty,
                                    back_defence,
                                    back_type_line,
                                    back_oracle_text)
        """

    await asyncio.gather(
        pool.execute(rule_index),
        pool.execute(card_index),
        pool.execute(distinct_cards_ix),
        return_exceptions=False
    )


