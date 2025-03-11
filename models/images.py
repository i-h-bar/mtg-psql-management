from pydantic import BaseModel


class Image(BaseModel):
    id: str | None
    scryfall_url: str | None
