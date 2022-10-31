import pandas as pd
import sqlite3
from pathlib import Path


connection = sqlite3.connect(str(Path(__file__).parent / 'cats.db'))


def _df():
    # df = pd.read_excel("cats_data.xlsx", sheet_name="breeds1", usecols=["id", "name", "description"])
    # df.to_sql("breeds", con=connection, if_exists='append', index=False)
    df = pd.read_excel("cats_data.xlsx", sheet_name="cats", usecols=[
        "personid", "name", "breedid", "birth", "description"
    ])
    df.to_sql("catperson", con=connection, if_exists='append', index=False)
    return df


_df()

