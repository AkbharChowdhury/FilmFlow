from pydantic import BaseModel, ConfigDict, NonNegativeInt

class MovieGenre(BaseModel):
    model_config = ConfigDict(frozen=True)

    movie_id: NonNegativeInt
    genre_id: NonNegativeInt
