import os
import shutil
from unittest import TestCase
from src.interface.db_manager import DBManager


class TestDBManager(TestCase):

    def setUp(self):

        # Check if path exists, then remove it.
        test_dir = "db_output"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        # Now make the output directory.
        os.mkdir(test_dir)

        self.db_path = f"{test_dir}/test.db"
        self.db_manager = DBManager(self.db_path)

    def tearDown(self):
        pass

    def test_create_db_manager(self):
        db_manager = DBManager()
        print("DB Manager Created", db_manager)

    def test_check_db_exists(self):
        db_name = "real.db"
        exists = self.db_manager.check_if_database_exists(db_name)
        self.assertTrue(exists)

    def test_db_can_connect(self):
        connection = self.db_manager.connect()
        connection.close()

    def test_db_print_all_tables(self):
        self.db_manager.print_all_tables()
        pass

    def test_db_create_table(self):
        schema = {
            "name": "TEXT",
            "price": "INTEGER"
        }
        self.db_manager.create_table("MyCoolTable", schema)
        self.db_manager.print_all_tables()

    def test_db_insert_into_table(self):
        table_name = "pills"
        schema = {
            "name": "TEXT",
            "price": "INTEGER"
        }
        data = ["aspirin", "120"]
        self.db_manager.create_table(table_name, schema)
        self.db_manager.insert_into_table(table_name, data)
        self.db_manager.insert_into_table(table_name, ["fake1", "1000"])
        self.db_manager.insert_into_table(table_name, ["digoxin", "520"])
        self.db_manager.print_all_tables()
        self.db_manager.show_table_data(table_name)


    def test_db_can_create_table(self):
        pass

    def test_table_exists(self):
        pass

    def test_can_insert_name_into_db(self):
        fake_name = "Alice"
        db_manager = DBManager()
        db_manager.insert_new_user(fake_name)

        does_name_exist = db_manager.check_if_name_exits(fake_name)
        self.assertTrue(does_name_exist)
