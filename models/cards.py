from pydantic import BaseModel
from datetime import datetime


class Card(BaseModel):
    id: str
    oracle_id: str
    name: str
    normalised_name: str
    flavour_text: str
    release_date: datetime
    reserved: bool
    rarity: str
    artist_id: str
    image_id: str
    legality_id: str
    rule_id: str
    set_id: str
    backside_id: str = None
