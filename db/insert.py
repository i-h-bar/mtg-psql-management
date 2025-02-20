from asyncpg import Pool
from tqdm import tqdm

from db.queries import INSERT_ARTIST, INSERT_ILLUSTRATION, INSERT_IMAGE, INSERT_LEGALITY, INSERT_RULE, INSERT_SET, \
    INSERT_TOKEN, INSERT_CARD, INSERT_RELATED_CARD, INSERT_RELATED_TOKEN
from models.card_info import CardInfo
from utils.card_cache import artist_cache, illustration_cache, token_cache
from utils.parse import parse_card


async def _insert_card(card_info: CardInfo, pool: Pool):
    artist = card_info.artist
    if artist.id not in artist_cache:
        await pool.execute(INSERT_ARTIST, artist.id, artist.name, artist.normalised_name)
        artist_cache.add(artist.id)

    illustration = card_info.illustration
    if illustration.id not in illustration_cache:
        await pool.execute(INSERT_ILLUSTRATION, illustration.id, illustration.illustration)
        illustration_cache.add(illustration.id)

    image = card_info.image
    await pool.execute(INSERT_IMAGE, image.id, image.png)

    legality = card_info.legality
    await pool.execute(
        INSERT_LEGALITY, legality.id, legality.alchemy, legality.brawl, legality.commander,
        legality.duel, legality.explorer, legality.future, legality.gladiator, legality.historic,
        legality.legacy, legality.modern, legality.oathbreaker, legality.oldschool, legality.pauper,
        legality.paupercommander, legality.penny, legality.pioneer, legality.predh, legality.premodern,
        legality.standard, legality.standardbrawl, legality.timeless, legality.vintage
    )

    rule = card_info.rule
    await pool.execute(
        INSERT_RULE, rule.id, rule.colour_identity, rule.mana_cost, rule.cmc, rule.power, rule.toughness,
        rule.loyalty, rule.defence, rule.type_line, rule.oracle_text, rule.colours, rule.keywords,
        rule.produced_mana
    )

    set_ = card_info.set
    await pool.execute(INSERT_SET, set_.id, set_.name, set_.normalised_name, set_.abbreviation)

    card = card_info.card
    await pool.execute(
        INSERT_CARD, card.id, card.oracle_id, card.name, card.normalised_name, card.scryfall_url,
        card.flavour_text, card.release_date, card.reserved, card.rarity, card.artist_id, card.image_id,
        card.illustration_id, card.legality_id, card.rule_id, card.set_id
    )

    for related_token in card_info.related_tokens:
        await pool.execute(INSERT_RELATED_TOKEN, related_token.id, related_token.card_id, related_token.token_id)


async def insert_card(card: dict, pbar: tqdm, pool: Pool) -> None:
    card_infos = parse_card(card)
    if not card_infos:
        pbar.update()

    for card_info in card_infos:
        await _insert_card(card_info, pool)

    for card_info in card_infos:
        for related_card in card_info.related_cards:
            await pool.execute(
                INSERT_RELATED_CARD, related_card.id, related_card.card_id, related_card.related_card_id
            )

    pbar.update()
