import uuid
from datetime import datetime

from models.artists import Artist, MISSING_ID_ID, MISSING_ARTIST
from models.cards import Card
from models.images import Image
from models.legalities import Legality
from models.rules import Rule
from models.sets import Set
from utils.normalise import normalise



def produce_side(
        card: dict, side: dict, side_id: str, reverse_side_id: str, legality: Legality, set_: Set
) -> tuple[Card, Artist, Rule, Image]:
    artist_id = (side.get("artist_ids") or card.get("artist_ids") or MISSING_ID_ID)[0]
    artist_name = side.get("artist") or card.get("artist") or MISSING_ARTIST
    artist = Artist(
        id=artist_id,
        name=artist_name,
        normalised_name=normalise(artist_name),
    )

    rule = Rule(
        id=str(uuid.uuid4()),
        colour_identity=card["color_identity"],
        mana_cost=side.get("mana_cost"),
        cmc=card["cmc"],
        power=side.get("power"),
        toughness=side.get("toughness"),
        loyalty=side.get("loyalty"),
        defence=side.get("defense"),
        type_line=side["type_line"],
        oracle_text=side.get("oracle_text"),
        colours=side.get("colors", []),
        keywords=side.get("keywords", []),
        produced_mana=side.get("produced_mana"),
    )

    image = Image(
        id=str(uuid.uuid4()),
        png=side["image_uris"]["png"],
        art_crop=side["image_uris"]["art_crop"]
    )

    card = Card(
        id=side_id,
        oracle_id=card["oracle_id"],
        name=side["name"],
        normalised_name=normalise(side["name"]),
        scryfall_url=card["scryfall_uri"],
        flavour_text=side.get("flavor_text"),
        release_date=datetime.strptime(card["released_at"], "%Y-%m-%d"),
        reserved=card["reserved"],
        rarity=card["rarity"],
        artist_id=artist.id,
        image_id=image.id,
        legality_id=legality.id,
        rule_id=rule.id,
        set_id=set_.id,
        reverse_side_id=reverse_side_id,
    )

    return card, artist, rule, image


def produce_dual_faced_card(card: dict, front: dict, back: dict) -> tuple[
    tuple[Card, Artist, Rule, Legality, Image, Set],
    tuple[Card, Artist, Rule, Legality, Image, Set]
]:
    back_id = str(uuid.uuid4())

    legality = Legality(
        id=str(uuid.uuid4()),
        **card["legalities"],
    )

    set_ = Set(
        id=card["set_id"],
        name=card["set_name"],
        normalised_name=normalise(card["set_name"]),
        abbreviation=card["set"],
    )

    front_card, front_artist, front_rule, front_image = produce_side(card, front, card["id"], back_id, legality, set_)
    back_card, back_artist, back_rule, back_image = produce_side(card, back, back_id, front_card.id, legality, set_)

    return (
        (front_card, front_artist, front_rule, legality, front_image, set_),
        (back_card, back_artist, back_rule, legality, back_image, set_)
    )