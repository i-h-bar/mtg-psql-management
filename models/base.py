from pydantic import BaseModel

from models.artists import Artist
from models.cards import Card
from models.illustrations import Illustration
from models.images import Image
from models.legalities import Legality
from models.related_cards import RelatedCard
from models.related_tokens import RelatedToken
from models.rules import Rule
from models.sets import Set
from models.tokens import Token


class CardInfo(BaseModel):
    card: Card
    artist: Artist
    legality: Legality
    image: Image
    illustration: Illustration
    rule: Rule
    set: Set
    related_card: list[RelatedCard] = None
    token: list[Token] = None
    related_token: list[RelatedToken] = None
