from pydantic import BaseModel, Field

from models.artists import Artist
from models.cards import Card
from models.combos import Combo
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set


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
