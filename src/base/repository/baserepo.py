import sqlite3
import os
from database.create_database import DB_NAME

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseRepo:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn