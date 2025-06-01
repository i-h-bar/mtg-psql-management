from pydantic import BaseModel, Field

from src.models.artists import Artist
from src.models.cards import Card
from src.models.combos import Combo
from src.models.illustrations import Illustration
from src.models.images import Image
from src.models.legalities import Legality
from src.models.related_tokens import RelatedToken
from src.models.rules import Rule
from src.models.sets import Set


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
