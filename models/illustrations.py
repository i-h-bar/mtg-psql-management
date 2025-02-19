from pydantic import BaseModel


class Illustration(BaseModel):
    id: str
    illustration: str
