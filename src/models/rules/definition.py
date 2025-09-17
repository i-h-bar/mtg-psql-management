from pydantic import BaseModel


class Definition(BaseModel):
    term: str
    definition: str
    rules_reference: list[str]
