from typing import Self

from pydantic import BaseModel

from utils.custom_types import JSONType


class Rule(BaseModel):
    id: str
    colour_identity: list[str]
    mana_cost: str | None
    cmc: float
    power: str | None
    toughness: str | None
    loyalty: str | None
    defence: str | None
    type_line: str | None
    oracle_text: str | None
    colours: list[str] | None
    keywords: list[str] | None
    produced_mana: list[str] | None
    rulings_url: str | None

    @classmethod
    def from_card(cls: type[Self], card: dict[str, JSONType]) -> Self:
        return cls(
            id=card["oracle_id"],
            colour_identity=card["color_identity"],
            mana_cost=card["mana_cost"],
            cmc=card.get("cmc", 0.0),
            power=card.get("power"),
            toughness=card.get("toughness"),
            loyalty=card.get("loyalty"),
            defence=card.get("defense"),
            type_line=card["type_line"],
            oracle_text=card.get("oracle_text"),
            colours=card.get("colors", []),
            keywords=card.get("keywords", []),
            produced_mana=card.get("produced_mana"),
            rulings_url=card.get("rulings_uri"),
        )
