from pydantic import BaseModel


class Image(BaseModel):
    id: str
    scryfall_url: str
    png: str | None = None
