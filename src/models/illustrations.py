from __future__ import annotations

from typing import Self

from pydantic import BaseModel

from utils.custom_types import JSONType

illustration_cache: dict[str, Illustration] = {}


class Illustration(BaseModel):
    id: str
    scryfall_url: str

    @classmethod
    def from_card(cls: type[Self], card: dict[str, JSONType]) -> Self | None:
        if not (illustration_id := card.get("illustration_id")):
            return None

        if not (illustration := illustration_cache.get(illustration_id)):
            illustration = cls(id=illustration_id, scryfall_url=card["image_uris"]["art_crop"])
            illustration_cache[illustration_id] = illustration
            return illustration

        return illustration
