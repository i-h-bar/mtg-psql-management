import uuid

from pydantic import BaseModel, Field


class RelatedToken(BaseModel):
    card_id: str
    token_id: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
