from typing import Self

from pydantic import BaseModel

from utils.custom_types import JSONType
from utils.normalise import normalise

MISSING_ID_ID = ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]
MISSING_ARTIST = "Anonymous"


class Artist(BaseModel):
    id: str
    name: str
    normalised_name: str

    @classmethod
    def from_card(cls: type[Self], card: dict[str, JSONType]) -> Self:
        return cls(
            id=card.get("artist_ids", MISSING_ID_ID)[0],
            name=card["artist"] or MISSING_ARTIST,
            normalised_name=normalise(card["artist"] or MISSING_ARTIST),
        )
