import uuid
from datetime import datetime

from models.card_info import CardInfo
from models.illustrations import Illustration
from models.artists import Artist, MISSING_ID_ID, MISSING_ARTIST
from models.cards import Card
from models.images import Image
from models.legalities import Legality
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set
from models.tokens import Token
from utils.normalise import normalise


def produce_card(card: dict) -> CardInfo:
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
        png=card["image_uris"]["png"]
    )

    illustration = Illustration(
        id=card.get("illustration_id", MISSING_ARTIST),
        illustration=card["image_uris"]["art_crop"]
    )

    set_ = Set(
        id=card["set_id"],
        name=card["set_name"],
        normalised_name=normalise(card["set_name"]),
        abbreviation=card["set"],
    )

    card_model = Card(
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
        illustration_id=illustration.id,
        legality_id=legality.id,
        rule_id=rule.id,
        set_id=set_.id,
    )

    collected_tokens = []
    related_tokens = []
    if parts := card.get("all_parts"):
        if tokens := [part for part in parts if part["component"] == "token"]:
            for token in tokens:
                collected_tokens.append(
                    Token(
                        id=token["id"],
                        name=token["name"],
                        normalised_name=normalise(token["name"]),
                        scryfall_uri=token["uri"]
                    )
                )

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
        legality=legality,
        image=image,
        illustration=illustration,
        set=set_,
        tokens=collected_tokens,
        related_tokens=related_tokens,
    )