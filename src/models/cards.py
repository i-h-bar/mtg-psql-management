from datetime import datetime

from pydantic import BaseModel


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
