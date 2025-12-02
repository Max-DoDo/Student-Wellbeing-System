import sqlite3

class Base_Repo_test:

    # class-level shared DB path
    DB_PATH_test = None

    def __init__(self):
        if self.DB_PATH_test is None:
            raise RuntimeError("DB_PATH_test is not set. Call BaseRepo_test.set_db_path_test() before creating repo objects.")
        self.conn = sqlite3.connect(self.DB_PATH_test)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    @classmethod
    def set_db_path_test(cls, path: str):
        cls.DB_PATH_test = path

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
