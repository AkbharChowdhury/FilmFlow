from typing import Any, Optional, Dict

from psycopg2.extras import DictCursor
from psycopg2 import connect
from config import load_config
from contextlib import contextmanager

from models.genres import Genre
from models.movie_genres import MovieGenre


@contextmanager
def get_cursor(
        query: None,
        params: Optional[Dict[str, Any]] = None,
        cursor_factory: Optional[Any] = None
):
    if params is None:
        params = {}
    with connect(**load_config()) as conn, conn.cursor(cursor_factory=cursor_factory) as cursor:
        cursor.execute(query, params)
        yield cursor


def field(name: str) -> str:
    """Format a field name as a parameter placeholder: e.g. 'title' → '%(title)s'"""
    return f"%({name})s"


class FilmFlowDB:

    def fetch_movies(self, title: str = "", genre="") -> list:
        query = """
            SELECT movie_id, title, genres
            FROM fn_get_movies(%s, %s)
        """
        params = (f"%{title}%", f"%{genre}%")

        with get_cursor(query=query, params=params, cursor_factory=DictCursor) as cursor:
            movies = (dict(row) for row in cursor.fetchall())
            return list(movies)

    def fetch_available_genres(self) -> list[Genre]:
        with get_cursor(query="SELECT genre, genre_id FROM available_movie_genres",
                        cursor_factory=DictCursor) as cursor:
            return list((Genre(name=row['genre'], genre_id=row['genre_id']) for row in cursor.fetchall()))

    def fetch_all_genres(self) -> list[Genre]:
        with get_cursor(query="SELECT genre AS name, genre_id FROM genres ORDER BY genre",
                        cursor_factory=DictCursor) as cursor:
            return list(Genre(**dict(row)) for row in cursor.fetchall())

    def add_movie_and_genres(self, title: str, genres: set[int]) -> None:
        with get_cursor(query="CALL pr_add_movie_and_genres(%s,%s)", params=(title, str(genres)),
                        cursor_factory=DictCursor) as cursor:
            pass

    def update_movie_title(self, movie_id: int, title: str) -> None:
        query = f"""
               UPDATE movies
               SET title = {field('title')}
               WHERE movie_id = {field('movie_id')}
           """
        params = {"title": title, "movie_id": movie_id}
        with get_cursor(query=query, params=params):
            pass

    def delete_record(self, id_field: str, table: str, num: int) -> None:
        params = {"num": num}
        with get_cursor(query=f"DELETE FROM {table} WHERE {id_field} = {field('num')}", params=params):
            pass

    def add_movie_genres(self, movie_id: int, genre_id_list: set[int]) -> None:
        query = f'''
            INSERT INTO movie_genres (movie_id, genre_id)
            VALUES ({field('movie_id')}, {field('genre_id')})
        '''
        for genre_id in genre_id_list:
            row: dict[str, int] = MovieGenre(movie_id=movie_id, genre_id=genre_id).model_dump()
            with get_cursor(query=query, params=row):
                pass
