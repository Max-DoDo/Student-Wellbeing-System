import sqlite3

class Base_Repo:

    # class-level shared DB path
    DB_PATH = None

    def __init__(self):
        if self.DB_PATH is None:
            raise RuntimeError("DB_PATH is not set. Call BaseRepo.set_db_path() before creating repo objects.")
        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    @classmethod
    def set_db_path(cls, path: str):
        cls.DB_PATH = path

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.conn.close()