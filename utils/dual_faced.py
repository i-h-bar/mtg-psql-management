import uuid
from datetime import datetime

from models.artists import Artist, MISSING_ID_ID, MISSING_ARTIST
from models.card_info import CardInfo
from models.cards import Card
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.related_cards import RelatedCard
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set
from utils.normalise import normalise



def produce_side(
        card: dict, side: dict, side_id: str, reverse_side_id: str, legality: Legality, set_: Set
) -> CardInfo:
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
        cmc=card.get("cmc", 0.0),
        power=side.get("power"),
        toughness=side.get("toughness"),
        loyalty=side.get("loyalty"),
        defence=side.get("defense"),
        type_line=side.get("type_line"),
        oracle_text=side.get("oracle_text"),
        colours=side.get("colors", []),
        keywords=side.get("keywords", []),
        produced_mana=side.get("produced_mana"),
    )

    image_uris = side.get("image_uris") or card.get("image_uris")

    image = Image(
        id=str(uuid.uuid4()),
        png=image_uris["png"]
    )

    illustration = Illustration(
        id=side.get("illustration_id") or card.get("illustration_id", str(uuid.uuid4())),
        illustration=image_uris["art_crop"]
    )

    card_model = Card(
        id=side_id,
        oracle_id=card.get("oracle_id", str(uuid.uuid4())),
        name=side["name"],
        normalised_name=normalise(side["name"]),
        scryfall_url=card["scryfall_uri"],
        flavour_text=side.get("flavor_text"),
        release_date=datetime.strptime(card["released_at"], "%Y-%m-%d"),
        reserved=card["reserved"],
        rarity=card["rarity"],
        artist_id=artist.id,
        image_id=image.id,
        illustration_id=illustration.id,
        legality_id=legality.id,
        rule_id=rule.id,
        set_id=set_.id,
    )

    related_cards = [
        RelatedCard(
            id=str(uuid.uuid4()),
            card_id=card_model.id,
            related_card_id=reverse_side_id,
        )
    ]

    related_tokens = []
    if parts := card.get("all_parts"):
        if tokens := [part for part in parts if part["component"] == "token"]:
            for token in tokens:
                related_tokens.append(
                    RelatedToken(
                        id=str(uuid.uuid4()),
                        token_id=token["id"],
                        card_id=card_model.id
                    )
                )

    return CardInfo(
        card=card_model,
        artist=artist,
        rule=rule,
        image=image,
        illustration=illustration,
        legality=legality,
        set=set_,
        related_cards=related_cards,
        related_tokens=related_tokens
    )


def produce_dual_faced_card(card: dict, front: dict, back: dict) -> tuple[CardInfo, CardInfo]:
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

    front = produce_side(card, front, card["id"], back_id, legality, set_)
    back = produce_side(card, back, back_id, front.card.id, legality, set_)

    return front, back