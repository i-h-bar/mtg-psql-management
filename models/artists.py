from pydantic import BaseModel

MISSING_ID_ID = ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]
MISSING_ARTIST = "Anonymous"


class Artist(BaseModel):
    id: str
    name: str
    normalised_name: str
