from pydantic import BaseModel


class Image(BaseModel):
    id: str
    png: str
    art_crop: str