import uuid
from datetime import datetime

from models.artists import Artist, MISSING_ID_ID, MISSING_ARTIST
from models.cards import Card
from models.images import Image
from models.legalities import Legality
from models.rules import Rule
from models.sets import Set
from utils.normalise import normalise


def produce_card(card: dict) -> tuple[Card, Artist, Rule, Legality, Image, Set]:
    artist = Artist(
        id=card.get("artist_ids", MISSING_ID_ID)[0],
        name=card["artist"] or MISSING_ARTIST,
        normalised_name=normalise(card["artist"] or MISSING_ARTIST),
    )

    rule = Rule(
        id=str(uuid.uuid4()),
        colour_identity=card["color_identity"],
        mana_cost=card["mana_cost"],
        cmc=card["cmc"],
        power=card.get("power"),
        toughness=card.get("toughness"),
        loyalty=card.get("loyalty"),
        defence=card.get("defense"),
        type_line=card["type_line"],
        oracle_text=card["oracle_text"],
        colours=card.get("colors", []),
        keywords=card.get("keywords", []),
        produced_mana=card.get("produced_mana"),
    )

    legality = Legality(
        id=str(uuid.uuid4()),
        **card["legalities"],
    )

    image = Image(
        id=str(uuid.uuid4()),
        png=card["image_uris"]["png"],
        art_crop=card["image_uris"]["art_crop"]
    )

    set_ = Set(
        id=card["set_id"],
        name=card["set_name"],
        normalised_name=normalise(card["set_name"]),
        abbreviation=card["set"],
    )

    card = Card(
        id=card["id"],
        oracle_id=card["oracle_id"],
        name=card["name"],
        normalised_name=normalise(card["name"]),
        scryfall_url=card["scryfall_uri"],
        flavour_text=card.get("flavor_text"),
        release_date=datetime.strptime(card["released_at"], "%Y-%m-%d"),
        reserved=card["reserved"],
        rarity=card["rarity"],
        artist_id=artist.id,
        image_id=image.id,
        legality_id=legality.id,
        rule_id=rule.id,
        set_id=set_.id,
    )

    return card, artist, rule, legality, image, set_