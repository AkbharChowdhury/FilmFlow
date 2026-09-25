from pydantic import BaseModel, ConfigDict, NonNegativeInt, Field
from typing import Union, Any
from uuid import uuid4


class MovieGenre(BaseModel):
    model_config = ConfigDict(frozen=True)
    movie_id: NonNegativeInt
    genre_id: NonNegativeInt


class Genre(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    genre_id: Union[str, int] = Field(default_factory=lambda: str(uuid4()))


class Movie:
    @staticmethod
    def sort(movies: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for movie in movies:
            genre_string: str = movie["genres"]
            genres: list[str] = [genre.strip() for genre in genre_string.split("|")]
            sorted_genres: list[str] = sorted(genres, key=str.casefold)
            movie["genres"] = " | ".join(sorted_genres)
        movies = sorted(movies, key=lambda m: m["title"].casefold())
        return movies
