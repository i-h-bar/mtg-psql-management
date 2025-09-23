from pydantic import BaseModel


class Section(BaseModel):
    id: int
    title: str
