from psycopg2 import sql

from app.exceptions import AnimeNotFound
from app.models import DatabaseConnector
from app.services import validate_keys
from app.services.anime_service import validate_keys


class Anime(DatabaseConnector):
    table_name = "animes"
    FIELDNAMES = ["anime", "released_date", "seasons"]

    def __init__(self, **kwargs) -> None:

        self.anime = kwargs["anime"].title()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]
        validate_keys(self.__dict__.keys(), kwargs.keys())

    @classmethod
    def get_all(cls):
        return super().get_all(cls.table_name)

    def register_item(self):
        return super().register_item(self.__dict__, self.table_name)

    @classmethod
    def update_item(cls, item_id, payload):
        if payload["anime"]:
            payload["anime"] = payload["anime"].title()
        return super().update_item(item_id, payload, cls.table_name)

    @classmethod
    def delete_item(cls, item_id):
        return super().delete_item(item_id, cls.table_name)

    @classmethod
    def get_anime_by_id(cls, anime_id: int):
        cls.init_connection()

        query = """
            SELECT * 
            FROM animes
            WHERE 
                id = %s;
        """

        cls.cur.execute(query, [anime_id])

        anime = cls.cur.fetchone()

        if not anime:
            raise AnimeNotFound(anime_id)

        cls.close_connection(commit=False)

        return anime
