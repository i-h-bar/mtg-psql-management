from asyncpg import Pool
from tqdm import tqdm

from db.queries import INSERT_ARTIST
from utils.card_cache import artist_cache
from utils.parse import parse_card


async def insert_card(card: dict, pbar: tqdm, pool: Pool) -> None:
    card_infos = parse_card(card)
    if not card_infos:
        pbar.update()

    for card_info in card_infos:
        artist = card_info.artist
        if artist.id not in artist_cache:
            artist_cache.add(artist.id)
            await pool.execute(INSERT_ARTIST, artist.id, artist.name, artist.normalised_name)

    pbar.update()
