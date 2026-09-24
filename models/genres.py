from typing import Union
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Genre(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    genre_id: Union[str, int] = Field(default_factory=lambda: str(uuid4()))
