import sqlite3

SQLITE_KEY_TYPES = ["INTEGER", "TEXT", "BLOB", "REAL", 'TEXT NOT NULL', 'INTEGER NOT NULL']


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

    def teardown(self) -> None:
        """
        Cleanup everything after working with database.
        Do anything that may be needed or leave blank
        :return:
        """
        self.connection.close()


class KeysForTable:
    def __init__(self, int_primary_key_name: str = "id"):
        """
        Initialize primary key with INT value for table
        """
        self.primary_key = int_primary_key_name
        self.other_keys: dict = {}
        self.foreign_keys: list = []

    def create_keys(self, keys_dct: dict):
        for key_name in keys_dct:
            if keys_dct[key_name] in SQLITE_KEY_TYPES:
                self.other_keys[key_name] = keys_dct[key_name]

    def create_key(self, key_name: str, key_type: str):
        if key_type in SQLITE_KEY_TYPES:
            self.other_keys[key_name] = key_type

    def create_foreign_key(self, key_name: str, other_table_name: str, foreign_key: str):
        self.foreign_keys.append([key_name, other_table_name, foreign_key])

    def build_keys_list(self):
        keys_list = [f"\t\"{self.primary_key}\" INTEGER NOT NULL\n"]
        for key_name in self.other_keys:
            keys_list.append(f'\t\"{key_name}\" {self.other_keys[key_name]}\n')
        keys_list.append(f"PRIMARY KEY(\"{self.primary_key}\" AUTOINCREMENT)")
        for lst in self.foreign_keys:
            assert len(lst) == 3
            keys_list.append(f"\tFOREIGN KEY ({lst[0]})  REFERENCES {lst[1]} ({lst[2]})\n")
        return keys_list


class TableModify(DataBaseHandler):
    def create_table(self, table_name: str, keys: KeysForTable):
        super()._execute_str(
            f"CREATE TABLE IF NOT EXISTS \"{table_name}\" (\n".join(x for x in keys.build_keys_list()).join(")")
        )

    def delete_table(self, table_name: str):
        super()._execute_str(f"DROP TABLE IF EXISTS {table_name}")

    def rename_table(self, old_table_name: str, new_table_name: str):
        super()._execute_str(f"ALTER TABLE {old_table_name}\nRENAME TO {new_table_name}")

    def add_column(self, table_name: str, column_name: str, column_type: str):
        if column_type in SQLITE_KEY_TYPES:
            super()._execute_str(f"ALTER TABLE {table_name}\nADD COLUMN {column_name} {column_type}")

    def rename_column(self, table_name: str, old_column_name: str, new_column_name: str):
        super()._execute_str(f"ALTER TABLE {table_name}\nRENAME COLUMN {old_column_name} TO {new_column_name}")

    def delete_column(self, table_name: str, column_name: str):
        super()._execute_str(f"ALTER TABLE {table_name}]\nDROP COLUMN {column_name}")