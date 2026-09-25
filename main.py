from film_flow_db import FilmFlowDB
from models import Movie


def main():
    db = FilmFlowDB()
    movies = Movie.sort(db.fetch_movies(genre='comedy'))
    for movie in movies:
        print(f"{movie['title']} ({movie['genres']})")


if __name__ == "__main__":
    main()
