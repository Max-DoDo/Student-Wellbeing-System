import sqlite3
import os
from database.create_database import DB_NAME

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseRepo:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()