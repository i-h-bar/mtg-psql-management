from typing import Self

from pydantic import BaseModel

from utils.art_ids import parse_art_id
from utils.custom_types import JSONType


class Image(BaseModel):
    id: str | None
    scryfall_url: str | None

    @classmethod
    def from_card(cls: type[Self], card: dict[str, JSONType]) -> Self | None:
        if image_id := parse_art_id(card["image_uris"]["png"]):
            return cls(id=image_id, scryfall_url=card["image_uris"]["png"])

        return None
