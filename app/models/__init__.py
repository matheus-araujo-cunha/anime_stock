import psycopg2
from os import getenv
from dotenv import load_dotenv
from psycopg2 import sql, extras
from app.exceptions import AnimeNotFound

load_dotenv()


configs = {
    "host": getenv("DB_HOST"),
    "database": getenv("DB_NAME"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
}


class DatabaseConnector:
    DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        "DEC2FLOAT",
        lambda value, curs: float(value) if value is not None else None,
    )

    psycopg2.extensions.register_type(DEC2FLOAT)

    @classmethod
    def init_connection(cls):
        cls.conn = psycopg2.connect(**configs, cursor_factory=extras.RealDictCursor)
        cls.cur = cls.conn.cursor()

    @classmethod
    def create_or_check_table(cls):
        cls.init_connection()

        query = """
            CREATE TABLE IF NOT EXISTS animes(
                id             BIGSERIAL    PRIMARY KEY,
                anime          VARCHAR(100) NOT NULL UNIQUE,
                released_date  DATE         NOT NULL,
                seasons        INT          NOT NULL
            );
        """
        cls.cur.execute(query)
        cls.close_connection()

    @classmethod
    def close_connection(cls, commit=True):
        if commit:
            cls.conn.commit()

        cls.cur.close()
        cls.conn.close()

    @classmethod
    def get_all(cls, table_name: str):
        cls.init_connection()

        sql_table_name = sql.Identifier(table_name)

        query = sql.SQL(
            """
            SELECT * FROM {table};
        """
        ).format(table=sql_table_name)

        cls.cur.execute(query)
        all_items = cls.cur.fetchall()
        cls.close_connection(commit=False)

        return all_items

    @staticmethod
    def identifier_items(keys: list):
        return [sql.Identifier(key) for key in keys]

    @staticmethod
    def literal_items(values: list):
        return [sql.Literal(value) for value in values]

    def register_item(self, item: dict, table_name: str):
        self.init_connection()

        sql_table_name = sql.Identifier(table_name)
        sql_columns = [sql.Identifier(key) for key in item.keys()]
        sql_values = [sql.Literal(value) for value in item.values()]

        query = sql.SQL(
            """
            INSERT INTO
                {table}({columns})
            VALUES
                ({values})
            RETURNING *;
        """
        ).format(
            table=sql_table_name,
            columns=sql.SQL(",").join(sql_columns),
            values=sql.SQL(",").join(sql_values),
        )

        self.cur.execute(query)
        self.conn.commit()

        new_item = self.cur.fetchone()

        self.close_connection()

        return new_item

    @classmethod
    def update_item(cls, item_id: int, item: dict, table_name: str):
        cls.init_connection()

        sql_table_name = sql.Identifier(table_name)
        sql_columns = [sql.Identifier(key) for key in item.keys()]
        sql_values = [sql.Literal(value) for value in item.values()]
        sql_id = sql.Literal(item_id)

        query = sql.SQL(
            """
            UPDATE
                {table}
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}
            RETURNING *;
        """
        ).format(
            id=sql_id,
            table=sql_table_name,
            columns=sql.SQL(",").join(sql_columns),
            values=sql.SQL(",").join(sql_values),
        )

        cls.cur.execute(query)

        updated_item = cls.cur.fetchone()

        if not updated_item:
            raise AnimeNotFound(item_id)

        cls.close_connection()

        return updated_item

    @classmethod
    def delete_item(cls, item_id: int, table_name: str):
        cls.init_connection()

        sql_id = sql.Literal(item_id)
        sql_table_name = sql.Identifier(table_name)

        query = sql.SQL(
            """
            DELETE
            FROM {table}
            WHERE 
                id = {id}
            RETURNING *;
        """
        ).format(id=sql_id, table=sql_table_name)

        cls.cur.execute(query)

        deleted_item = cls.cur.fetchone()

        if not deleted_item:
            raise AnimeNotFound(item_id)

        cls.close_connection()

        return deleted_item


DatabaseConnector.create_or_check_table()
