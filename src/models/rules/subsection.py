from pydantic import BaseModel


class SubSection(BaseModel):
    id: int
    section_id: int
    title: str
