from pydantic import BaseModel


class Rule(BaseModel):
    id: str
    colour_identity: list[str]
    mana_cost: str
    cmc: float
    power: str | None
    toughness: str | None
    loyalty: str | None
    defence: str | None
    type_line: str
    oracle_text: str
    colours: list[str]
    keywords: list[str] | None
    produced_mana: list[str] | None

