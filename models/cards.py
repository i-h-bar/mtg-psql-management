from pydantic import BaseModel
from datetime import datetime


class Card(BaseModel):
    id: str
    oracle_id: str
    name: str
    normalised_name: str
    release_date: datetime




