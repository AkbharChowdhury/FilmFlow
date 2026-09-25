from typing import Any

from film_flow_db import FilmFlowDB


class Movie:
    @staticmethod
    def sort(movies: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for movie in movies:
            genre_string: str = movie["genres"]
            genres: list[str] = [genre.strip() for genre in genre_string.split("|")]
            sorted_genres: list[str] = sorted(genres, key=str.casefold)
            movie["genres"] = " | ".join(sorted_genres)
        sorted_movies = sorted(movies, key=lambda m: m["title"].casefold())
        return sorted_movies


def main():
    db = FilmFlowDB()
    movies = Movie.sort(db.fetch_movies(genre='comedy'))
    for movie in movies:
        print(f"{movie['title']} ({movie['genres']})")


if __name__ == "__main__":
    main()
