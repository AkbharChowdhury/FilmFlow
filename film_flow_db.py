from typing import Any, Optional, Dict

from psycopg2.extras import DictCursor, execute_values
from psycopg2 import connect
from config import load_config
from contextlib import contextmanager
from models import Genre


@contextmanager
def get_cursor(
        query: str,
        params: Optional[Dict[str, str]] = None,
        cursor_factory: Optional[Any] = None
):
    if params is None:
        params = {}
    with connect(**load_config()) as conn, conn.cursor(cursor_factory=cursor_factory) as cursor:
        cursor.execute(query, params)
        yield cursor


def field(name: str) -> str:
    """Format a field name as a parameter placeholder: e.g. 'title' → '%(title)s'"""
    return f'%({name})s'


class FilmFlowDB:

    def fetch_movies(self, title: str = "", genre=""):
        """
        Fetch movies by optional title and genre filters
        :param title: str
        :param genre: str
        """
        query: str = """
        SELECT movie_id, title, genres
        FROM fn_get_movies(%s, %s)
        """
        params = (f"%{title.strip()}%", f"%{genre.strip()}%")

        with get_cursor(query, params, cursor_factory=DictCursor) as movies:
            for movie in movies:
                yield dict(movie)

    def fetch_available_genres(self) -> list[Genre]:
        query: str = 'SELECT genre, genre_id FROM available_movie_genres'
        with get_cursor(query=query, cursor_factory=DictCursor) as genres:
            return list((Genre(name=genre['genre'], genre_id=genre['genre_id']) for genre in genres.fetchall()))

    def fetch_all_genres(self) -> list[Genre]:
        query: str = 'SELECT genre AS name, genre_id FROM genres ORDER BY genre'
        with get_cursor(query=query, cursor_factory=DictCursor) as genres:
            return list(Genre(**dict(genre)) for genre in genres.fetchall())

    def add_movie_and_genres(self, title: str, genres: set[int]) -> None:
        query: str = 'CALL pr_add_movie_and_genres(%s, %s)'
        with get_cursor(query=query, params=(title, str(genres)), cursor_factory=DictCursor) as _:
            pass

    def update_movie_title(self, movie_id: int, title: str) -> None:
        query: str = f"""
               UPDATE movies
               SET title = {field('title')}
               WHERE movie_id = {field('movie_id')}
           """
        params: dict[str, Any] = {
            'title': title,
            'movie_id': movie_id
        }
        with get_cursor(query=query, params=params):
            pass

    def delete_record(self, id_field: str, table: str, num: int) -> None:
        params = {'num': num}
        query: str = f"DELETE FROM {table} WHERE {id_field} = {field('num')}"
        with get_cursor(query=query, params=params):
            pass

    def add_movie_genres(self, movie_id: int, genre_id_set: set[int]) -> None:
        query: str = 'INSERT INTO movie_genres (movie_id, genre_id) VALUES %s'
        with connect(**load_config()) as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
            execute_values(
                cursor,
                query,
                [(movie_id, genre_id) for genre_id in genre_id_set],
            )
