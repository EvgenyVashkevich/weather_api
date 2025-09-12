from pydantic import BaseModel, Field


class NotFound(BaseModel):
    error: str = Field('city not found')
