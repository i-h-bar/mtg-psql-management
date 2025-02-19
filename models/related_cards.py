from pydantic import BaseModel


class RelatedCard(BaseModel):
    id: str
    card_id: str
    related_card_id: str
