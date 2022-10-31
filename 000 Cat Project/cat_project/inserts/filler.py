import sqlite3
from pypika import Query, Table
from pathlib import Path

# from ..db_structure import DataBaseHandler


class DataBaseHandler:
    def __init__(self, sqlite_database_name: str):
        """
        Initialize all the context for working with database here
        :param sqlite_database_name: path to the sqlite3 database file
        """
        self.connection = sqlite3.connect(sqlite_database_name)

    def _execute_str(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def _commit(self):
        self.connection.commit()

    def _execute_str_tuple(self, query: str, tpl: tuple):
        cursor = self.connection.cursor()
        cursor.execute(query, tpl)
        return cursor.fetchall()

    def teardown(self) -> None:
        """
        Cleanup everything after working with database.
        Do anything that may be needed or leave blank
        :return:
        """
        self.connection.close()


class DataBaseFiller(DataBaseHandler):

    def _execute_pypika(self, query: Query):
        cursor = self.connection.cursor()
        cursor.execute(str(query))
        return cursor.fetchall()

    def get_table_info(self, table_name):
        cursor_fetchall = super()._execute_str(f'PRAGMA table_info(\"{table_name}\")')
        return [(x[1], x[2]) for x in cursor_fetchall]

    def fill_one_row(self, table_name, info: tuple):
        _str = "?, " * (len(info) - 1) + "?"
        super()._execute_str_tuple(f"INSERT INTO {table_name} VALUES({_str})", info)
        super()._commit()


def get_column_info(table_name):
    handler = DataBaseFiller(str(Path(__file__).parent / 'cats.db'))
    table_info = handler.get_table_info(table_name)
    handler.teardown()
    return table_info


def fill_one_row(table_name, info: tuple):
    handler = DataBaseFiller(str(Path(__file__).parent / 'cats.db'))
    handler.fill_one_row(table_name, info)
    handler.teardown()


# breed = (3, "Рэгдолл", "Порода крупных полудлинношерстных домашник кошек с голубыми глазами")
# print(fill_one_row('breeds', breed))
print(get_column_info('breeds'))
