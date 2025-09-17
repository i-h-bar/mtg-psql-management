from pydantic import BaseModel


class Rule(BaseModel):
    number: str
    parent: str
    section: int
    section_title: str
    subsection: int
    subsection_title: str
    content: str
