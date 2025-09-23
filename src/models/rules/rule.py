from pydantic import BaseModel


class Rule(BaseModel):
    number: str
    parent: str
    subsection_id: int
    content: str
