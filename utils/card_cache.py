from models.cards import Card
from models.tokens import Token

cached_cards: dict[str, Card] = {}
token_cache: dict[str, Token] = {}
artist_cache: set[str] = set()
