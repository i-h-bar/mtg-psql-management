from typing import Generator

from models.base import CardInfo
from utils.dual_faced import produce_dual_faced_card
from utils.single_faced import produce_card


def parse_card(card) -> CardInfo | tuple[CardInfo, CardInfo] | None:
    if card.get("set_type") == "memorabilia":
        return None

    if not (sides := card.get("card_faces")):
        return produce_card(card)
    else:
        return produce_dual_faced_card(card, sides[0], sides[1])