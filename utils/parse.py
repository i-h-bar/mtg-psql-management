from models.card_info import CardInfo
from utils.dual_faced import produce_dual_faced_card
from utils.single_faced import produce_card


def parse_card(card) -> tuple[CardInfo, ...] | None:
    if not (sides := card.get("card_faces")):
        if card := produce_card(card):
            return (card,)
        else:
            return None
    else:
        return produce_dual_faced_card(card, sides[0], sides[1])
