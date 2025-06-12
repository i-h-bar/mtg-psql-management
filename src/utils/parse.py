from models.card_info import CardInfo
from utils.dual_faced import produce_dual_faced_card


def parse_card(card: dict[str, str | int | list]) -> tuple[CardInfo, ...] | None:
    if not (sides := card.get("card_faces")):
        if card := CardInfo.single_sided(card):
            return (card,)
        return None
    return produce_dual_faced_card(card, sides[0], sides[1])
