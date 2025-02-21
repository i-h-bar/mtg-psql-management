import uuid

from pydantic import BaseModel, Field


class Combo(BaseModel):
    card_id: str
    combo_card_id: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
