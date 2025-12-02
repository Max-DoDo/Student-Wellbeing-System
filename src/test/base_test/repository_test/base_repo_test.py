import sqlite3

class Base_Repo_test:

    # class-level shared DB path
    DB_PATH_test = None

    def __init__(self):
        if self.DB_PATH_test is None:
            raise RuntimeError("DB_PATH_test is not set. Call BaseRepo_test.set_db_path_test() before creating repo objects.")
        self.conn_test = sqlite3.connect(self.DB_PATH_test)
        self.conn_test.row_factory = sqlite3.Row
        self.cursor_test = self.conn_test.cursor()

    @classmethod
    def set_db_path_test(cls, path: str):
        cls.DB_PATH_test = path

    def close_test(self):
        if self.conn_test:
            self.conn_test.close()

    def __del__(self):
        self.conn_test.close()
