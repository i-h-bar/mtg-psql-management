from utils.parse import parse_card


async def insert_card(card: dict) -> None:
    card_info = parse_card(card)
    if not card_info:
        return

