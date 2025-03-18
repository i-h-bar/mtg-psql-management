import re
from uuid import UUID

art_id_regex = re.compile(
    r"https://cards\.scryfall\.io/(png|art_crop)/(front|back)/[0-9a-fA-F]/[0-9a-fA-F]/([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\.(png|jpg)\?\d+"
)

add = {
    "front": 0,
    "back": 1,
}

def parse_art_id(scryfall_url: str | None) -> str | None:
    if not scryfall_url:
        return None

    match = art_id_regex.match(scryfall_url)

    try:
        image_id = match.group(3)
    except AttributeError:
        return None

    side = match.group(2)
    if side == "front":
        return image_id
    else:
        new_id = int(UUID(image_id).hex, base=16) + add[side]
        return str(UUID(int=new_id))