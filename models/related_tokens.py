from pydantic import BaseModel


class RelatedToken(BaseModel):
    id: str
    card_id: str
    token_id: str
