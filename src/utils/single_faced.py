from models.artists import Artist
from models.card_info import CardInfo
from models.cards import Card
from models.combos import Combo
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.price import Price
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set
from utils.art_ids import parse_art_id
from utils.custom_types import JSONType
from utils.normalise import normalise


def produce_card(card: dict[str, JSONType]) -> CardInfo | None:
    if image_id := parse_art_id(card["image_uris"]["png"]):
        image = Image(id=image_id, scryfall_url=card["image_uris"]["png"])
    else:
        return None

    artist = Artist.from_card(card)
    rule = Rule(
        id=card["oracle_id"],
        colour_identity=card["color_identity"],
        mana_cost=card["mana_cost"],
        cmc=card.get("cmc", 0.0),
        power=card.get("power"),
        toughness=card.get("toughness"),
        loyalty=card.get("loyalty"),
        defence=card.get("defense"),
        type_line=card["type_line"],
        oracle_text=card.get("oracle_text"),
        colours=card.get("colors", []),
        keywords=card.get("keywords", []),
        produced_mana=card.get("produced_mana"),
        rulings_url=card.get("rulings_uri"),
    )

    legality = Legality(
        id=card["oracle_id"],
        game_changer=card.get("game_changer"),
        **card["legalities"],
    )

    illustration = Illustration.from_card(card)

    set_ = Set(
        id=card["set_id"],
        name=card["set_name"],
        normalised_name=normalise(card["set_name"]),
        abbreviation=card["set"],
    )

    card_model = Card.from_card(card, artist, image, set_, illustration)

    price = Price.from_card(card)

    combos = []
    related_tokens = []
    if parts := card.get("all_parts"):
        for part in parts:
            if part["component"] == "token":
                related_tokens.append(RelatedToken(token_id=part["id"], card_id=card_model.id))
            elif part["component"] == "compo_piece":
                combos.append(Combo(card_id=card_model.id, combo_card_id=part["id"]))

    return CardInfo(
        card=card_model,
        artist=artist,
        rule=rule,
        legality=legality,
        image=image,
        illustration=illustration,
        set=set_,
        related_tokens=related_tokens,
        combos=combos,
        price=price,
    )
