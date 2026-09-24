from film_flow_db import FilmFlowDB

if __name__ == "__main__":

    db = FilmFlowDB()

    for movie in db.fetch_movies(genre='Comedy'):
        print(movie)
