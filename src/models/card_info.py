from typing import Self

from pydantic import BaseModel, Field

from models.artists import Artist
from models.cards import Card
from models.combos import Combo, extract_combos
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.price import Price
from models.related_tokens import RelatedToken, extract_tokens
from models.rules import Rule
from models.sets import Set
from utils.custom_types import JSONType


class CardInfo(BaseModel):
    card: Card
    artist: Artist
    legality: Legality
    image: Image
    illustration: Illustration | None
    rule: Rule
    set: Set
    related_tokens: list[RelatedToken] = Field(default_factory=list)
    combos: list[Combo] = Field(default_factory=list)
    price: Price

    @classmethod
    def single_sided(cls: type[Self], card: dict[str, JSONType]) -> Self | None:
        image = Image.from_card(card)
        if not image:
            return None

        artist = Artist.from_card(card)
        rule = Rule.from_card(card)
        legality = Legality.from_card(card)
        illustration = Illustration.from_card(card)
        set_ = Set.from_card(card)
        card_model = Card.from_card(card, artist, image, set_, illustration)
        price = Price.from_card(card)

        combos = extract_combos(card)
        related_tokens = extract_tokens(card)

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
