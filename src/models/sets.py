from pydantic import BaseModel


class Set(BaseModel):
    id: str
    name: str
    normalised_name: str
    abbreviation: str
