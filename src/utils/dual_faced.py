import uuid
from datetime import datetime

from models.artists import MISSING_ARTIST, MISSING_ID_ID, Artist
from models.card_info import CardInfo
from models.cards import Card
from models.combos import Combo
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set
from utils.art_ids import parse_art_id
from utils.custom_types import JSONType
from utils.maths import increment_uuid
from utils.normalise import normalise
from utils.single_faced import illustration_cache


def produce_side(
    card: dict,
    side: dict,
    side_id: str,
    side_oracle_id: str,
    reverse_side_id: str,
    set_: Set,
) -> CardInfo | None:
    image_uris = side.get("image_uris") or card.get("image_uris")
    if image_uris and (image_id := parse_art_id(image_uris.get("png"))):
        image = Image(id=image_id, scryfall_url=image_uris["png"])
    else:
        return None

    artist_id = (side.get("artist_ids") or card.get("artist_ids") or MISSING_ID_ID)[0]
    artist_name = side.get("artist") or card.get("artist") or MISSING_ARTIST
    artist = Artist(
        id=artist_id,
        name=artist_name,
        normalised_name=normalise(artist_name),
    )

    legality = Legality(
        id=side_oracle_id,
        game_changer=card.get("game_changer"),
        **card["legalities"],
    )

    rule = Rule(
        id=side_oracle_id,
        colour_identity=card["color_identity"],
        mana_cost=side.get("mana_cost"),
        cmc=card.get("cmc", 0.0),
        power=side.get("power"),
        toughness=side.get("toughness"),
        loyalty=side.get("loyalty"),
        defence=side.get("defense"),
        type_line=side.get("type_line"),
        oracle_text=side.get("oracle_text"),
        colours=card.get("colors", []),
        keywords=card.get("keywords", []),
        produced_mana=side.get("produced_mana"),
        rulings_url=card.get("rulings_uri"),
    )

    if not side.get("illustration_id") and not card.get("illustration_id"):
        illustration = None

    elif not (illustration := illustration_cache.get(side.get("illustration_id") or card["illustration_id"])):
        illustration = Illustration(
            id=side.get("illustration_id") or card["illustration_id"],
            scryfall_url=image_uris["art_crop"],
        )
        illustration_cache[side.get("illustration_id") or card["illustration_id"]] = illustration

    card_model = Card(
        id=side_id,
        oracle_id=side_oracle_id,
        name=side["name"],
        normalised_name=normalise(side["name"]),
        scryfall_url=card["scryfall_uri"],
        flavour_text=side.get("flavor_text"),
        release_date=datetime.strptime(card["released_at"], "%Y-%m-%d"),
        reserved=card["reserved"],
        rarity=card["rarity"],
        artist_id=artist.id,
        image_id=image.id,
        illustration_id=None if not illustration else illustration.id,
        legality_id=legality.id,
        rule_id=rule.id,
        set_id=set_.id,
        backside_id=reverse_side_id,
    )

    combos = []
    related_tokens = []
    if parts := card.get("all_parts"):
        for part in parts:
            if part["component"] == "token":
                related_tokens.append(RelatedToken(token_id=part["id"], card_id=card_model.id))
            elif part["component"] == "combo_piece":
                combos.append(Combo(card_id=card_model.id, combo_card_id=part["id"]))

    return CardInfo(
        card=card_model,
        artist=artist,
        rule=rule,
        image=image,
        illustration=illustration,
        legality=legality,
        set=set_,
        related_tokens=related_tokens,
        combos=combos,
    )


def produce_dual_faced_card(
    card: dict[str, JSONType], front: dict[str, JSONType], back: dict[str, JSONType]
) -> tuple[CardInfo, CardInfo] | None:
    back_id = increment_uuid(card["id"])
    front_oracle_id = front.get("oracle_id") or card.get("oracle_id")
    back_oracle_id = increment_uuid(front_oracle_id)

    set_ = Set(
        id=card["set_id"],
        name=card["set_name"],
        normalised_name=normalise(card["set_name"]),
        abbreviation=card["set"],
    )

    front = produce_side(card, front, card["id"], front_oracle_id, back_id, set_)
    if not front:
        return None

    back = produce_side(card, back, back_id, back_oracle_id, front.card.id, set_)
    if not back:
        return None

    return front, back
