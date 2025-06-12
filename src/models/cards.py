from datetime import datetime
from typing import Self

from pydantic import BaseModel

from models.artists import Artist
from models.illustrations import Illustration
from models.images import Image
from models.sets import Set
from utils.custom_types import JSONType
from utils.normalise import normalise


class Card(BaseModel):
    id: str
    oracle_id: str
    name: str
    normalised_name: str
    scryfall_url: str
    flavour_text: str | None
    release_date: datetime
    reserved: bool
    rarity: str
    artist_id: str
    image_id: str | None
    illustration_id: str | None
    set_id: str
    backside_id: str | None = None

    @classmethod
    def from_card(
        cls: type[Self], card: dict[str, JSONType], artist: Artist, image: Image, set_: Set, illustration: Illustration
    ) -> Self:
        return cls(
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
            illustration_id=None if not illustration else illustration.id,
            set_id=set_.id,
        )
