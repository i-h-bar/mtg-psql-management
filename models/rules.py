from pydantic import BaseModel


class Rule(BaseModel):
    id: str
    legalities_id: str
    mana_cost: str
    cmc: int
    type_line: str
    oracle_text: str
    colours: list[str]
    colour_identity: list[str]
    keywords: list[str]