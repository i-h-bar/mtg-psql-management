import asyncio

from asyncpg import Pool
from tqdm import tqdm

from db import queries
from db.delete import delete_index_and_mv
from db.index import add_indexes
from db.materialized_view import create_mv_distinct, create_mv_for_artist, create_mv_for_set
from db.post_bulk_inserts import insert_combos, insert_token_relations
from models.card_info import CardInfo
from models.post_inserts import combo_relations, token_relations
from utils.card_cache import artist_cache, illustration_cache
from utils.combo_updates import update_combos
from utils.custom_types import JSONType
from utils.parse import parse_card


async def _insert_card(card_info: CardInfo, pool: Pool) -> None:
    artist = card_info.artist
    if artist.id not in artist_cache:
        await pool.execute(queries.artist.INSERT, artist.id, artist.name, artist.normalised_name)
        artist_cache.add(artist.id)

    illustration = card_info.illustration
    if illustration and illustration.id not in illustration_cache:
        await pool.execute(queries.illustration.INSERT, illustration.id, illustration.scryfall_url)
        illustration_cache.add(illustration.id)

    image = card_info.image
    await pool.execute(queries.image.INSERT, image.id, image.scryfall_url)

    legality = card_info.legality
    await pool.execute(
        queries.legality.UPSERT,
        legality.id,
        legality.alchemy,
        legality.brawl,
        legality.commander,
        legality.duel,
        legality.explorer,
        legality.future,
        legality.gladiator,
        legality.historic,
        legality.legacy,
        legality.modern,
        legality.oathbreaker,
        legality.oldschool,
        legality.pauper,
        legality.paupercommander,
        legality.penny,
        legality.pioneer,
        legality.predh,
        legality.premodern,
        legality.standard,
        legality.standardbrawl,
        legality.timeless,
        legality.vintage,
        legality.game_changer,
    )

    rule = card_info.rule
    await pool.execute(
        queries.rule.UPSERT,
        rule.id,
        rule.colour_identity,
        rule.mana_cost,
        rule.cmc,
        rule.power,
        rule.toughness,
        rule.loyalty,
        rule.defence,
        rule.type_line,
        rule.oracle_text,
        rule.colours,
        rule.keywords,
        rule.produced_mana,
        rule.rulings_url,
    )

    set_ = card_info.set
    await pool.execute(queries.sets.INSERT, set_.id, set_.name, set_.normalised_name, set_.abbreviation)

    card = card_info.card
    await pool.execute(
        queries.card.INSERT,
        card.id,
        card.oracle_id,
        card.name,
        card.normalised_name,
        card.scryfall_url,
        card.flavour_text,
        card.release_date,
        card.reserved,
        card.rarity,
        card.artist_id,
        card.image_id,
        card.illustration_id,
        card.legality_id,
        card.rule_id,
        card.set_id,
        card.backside_id,
    )

    for related_token in card_info.related_tokens:
        token_relations.append(related_token)

    for combo in card_info.combos:
        combo_relations.append(combo)


async def insert_card(card: dict, pbar: tqdm, pool: Pool) -> None:
    card_infos = parse_card(card)
    if not card_infos:
        pbar.update()
        return

    for card_info in card_infos:
        await _insert_card(card_info, pool)

    pbar.update()


async def insert_missing_data(data: tuple[dict[str, JSONType], ...], pool: Pool) -> None:
    await delete_index_and_mv(pool)

    with tqdm(total=len(data)) as pbar:
        pbar.set_description("Inserting Cards")
        pbar.refresh()
        await asyncio.gather(*(insert_card(card, pbar, pool) for card in data))

    await insert_token_relations(pool)
    await insert_combos(pool)
    await update_combos(data, pool)

    await create_mv_distinct(pool)
    await add_indexes(pool)

    all_sets = await pool.fetchval("select array_agg(normalised_name) from set;") or []
    with tqdm(total=len(all_sets)) as pbar:
        pbar.set_description("Creating set MVs")
        pbar.refresh()
        await asyncio.gather(*(create_mv_for_set(set_, pool, pbar) for set_ in all_sets))

    all_artists = await pool.fetchval("select array_agg(normalised_name) from artist;")
    with tqdm(total=len(all_artists)) as pbar:
        pbar.set_description("Creating artist MVs")
        pbar.refresh()
        await asyncio.gather(*(create_mv_for_artist(artist, pool, pbar) for artist in all_artists))
