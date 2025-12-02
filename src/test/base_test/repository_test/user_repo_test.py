from typing import List, Optional
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.log import Log
from test.base_test.repository_test.base_repo_test import Base_Repo_test
from test.base_test.entity_test.user_test import User_test

class User_Repo_test(Base_Repo_test):

    def getUser(self,id : int) -> Optional[User_test]:
        query = "SELECT * FROM users WHERE users_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toUser(row)
        return None
    
    def getUserByUserName(self, username : str) -> Optional[User_test]:
        query = "SELECT * FROM users WHERE username = ?"
        Log.debug(username)
        self.cursor.execute(query,(username,))
        row = self.cursor.fetchone()
        if row:
            return self.toUser(row)
        return None

    def getAllUser(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toUsers(rows)
        return None

        

    def toUser(self,row) -> User_test:
        return User_test(
            id=row["users_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            username=row["username"],
            password=row["password"],
            role_id=row["role_id"],
            is_active=row["is_active"],
            created_at=row["created_at"]
        )

    def toUsers(self,rows) -> List[User_test]:
        return [self.toUser(row) for row in rows]