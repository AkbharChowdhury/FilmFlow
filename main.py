from film_flow_db import FilmFlowDB
from models import Movie


def display_films(movies: list[dict]):
    movies = Movie.sort(movies)
    for movie in movies:
        print(f"{movie['title']} ({movie['genres']})")


def add_film(movie: Movie):
    db.add_movie_and_genres(movie.title, movie.genres)


def main():
    movies: list[dict] = list(db.fetch_movies())
    display_films(Movie.sort(movies))


if __name__ == "__main__":
    db = FilmFlowDB()
    main()
