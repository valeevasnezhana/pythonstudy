import sqlite3
from pypika import Query, Table, Order
from pathlib import Path
from ..db_structure import DataBaseHandler

# connection = sqlite3.connect('cats.db')
# cursor = connection.cursor()


class InfoGetter(DataBaseHandler):

    def _execute_pypika(self, query: Query):
        cursor = self.connection.cursor()
        cursor.execute(str(query))
        return cursor.fetchall()

    def get_cat_info(self, cat_name: str):
        cats = Table('catperson')
        breeds = Table('breeds')
        query = Query.from_(cats) \
            .inner_join(breeds).using('breedid') \
            .where(cats.name.like(f'%{cat_name}%')) \
            .select(cats.name, cats.description, breeds.name)
        return self._execute_pypika(query)

    def get_breed_info(self, breed_name):
        breeds = Table('breeds')
        query = Query.from_(breeds) \
            .where(breeds.name.like(f'%{breed_name}%')) \
            .select(breeds.name, breeds.description)
        return self._execute_pypika(query)


def get_cat_info(name: str) -> str:
    handler = InfoGetter(str(Path(__file__).parent / 'cats.db'))
    cat_info = handler.get_cat_info(name)
    handler.teardown()
    try:
        return f"""имя: {cat_info[0][0]}\nописание: {cat_info[0][1]}\nпорода: {cat_info[0][2]}"""
    except IndexError:
        return "Такого котика пока нет ^-^"


def get_breed_info(breed_name: str):
    handler = InfoGetter(str(Path(__file__).parent / 'cats.db'))
    breed_info = handler.get_breed_info(breed_name)
    handler.teardown()
    try:
        return f'порода: {breed_info[0][0]}\nописание: {breed_info[0][1]}'
    except IndexError:
        return "Такой породы нет в базе данных"
