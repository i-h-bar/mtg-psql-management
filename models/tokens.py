from pydantic import BaseModel


class Token(BaseModel):
    id: str
    name: str
    normalised_name: str
    scryfall_uri: str
