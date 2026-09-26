from film_flow_db import FilmFlowDB
from models import Movie


def main():
    db = FilmFlowDB()
    movies: list[dict] = list(db.fetch_movies(genre='comedy'))
    movies = Movie.sort(movies)
    for movie in movies:
        print(f"{movie['title']} ({movie['genres']})")


if __name__ == "__main__":
    main()
