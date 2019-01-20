import os
import sqlite3


class DBManager:

    def __init__(self, name: str = "default.db"):
        print("__init__ from DBManager")
        self.db_name = name

    # Public --------------------------------------------

    def insert_new_user(self, name):
        pass

    def check_if_name_exits(self, name) -> bool:
        return False

    # Private --------------------------------------------

    def check_if_database_exists(self, db_path: str):
        return os.path.exists(db_path)

    def create(self, db_name: str):
        pass

    def connect(self):
        connection = sqlite3.connect(self.db_name)
        return connection

    def check_table_exists(self, table: str) -> bool:
        pass

    def create_table(self, table_name, schema):
        conn = self.connect()
        cursor = conn.cursor()

        # Turn dict into string.
        # TODO: Dict ordering could be a problem.
        schema_list = []
        for k in schema:
            value = schema[k]
            schema_list.append(k + " " + value)
        schema_string = ", ".join(schema_list)

        cursor.execute(f"CREATE TABLE {table_name} ({schema_string});")
        conn.commit()
        conn.close()

    def insert_into_table(self, table_name, data: list):
        conn = self.connect()
        cursor = conn.cursor()
        data_string = "'" + "', '".join(data) + "'"
        cursor.execute(f"INSERT INTO {table_name} VALUES ({data_string});")
        conn.commit()
        conn.close()

    def show_table_data(self, table_name, count: int = 5):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        print (cursor.fetchall())
        conn.close()

    # Debug ------------------------------------------------

    def print_all_tables(self):
        """ Print all the table names in this database. """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
