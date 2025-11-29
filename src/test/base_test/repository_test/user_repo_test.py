from typing import List, Optional
from tools.log import Log
from entity.user_test import User_test
from repository.base_repo_test import Base_Repo_test

class User_Repo_test(Base_Repo_test):

    def getUser_test(self,id_test : int) -> Optional[User_test]:
        query = "SELECT * FROM users WHERE users_id = ?"
        self.cursor_test.execute(query, (id_test,))
        row = self.cursor_test.fetchone()
        if row:
            return self.toUser_test(row)
        return None
    
    def getUserByUserName_test(self, username_test : str) -> Optional[User_test]:
        query = "SELECT * FROM users WHERE username = ?"
        Log.debug(username_test)
        self.cursor_test.execute(query,(username_test,))
        row = self.cursor_test.fetchone()
        if row:
            return self.toUser_test(row)
        return None

    def getAllUser_test(self):
        query = "SELECT * FROM users"
        self.cursor_test.execute(query)
        rows = self.cursor_test.fetchall()
        if rows:
            return self.toUsers_test(rows)
        return None

    def toUser_test(self,row) -> User_test:
        return User_test(
            id_test=row["users_id"],
            first_name_test=row["first_name"],
            last_name_test=row["last_name"],
            email_test=row["email"],
            username_test=row["username"],
            password_test=row["password"],
            role_id_test=row["role_id"],
            is_active_test=row["is_active"],
            created_at_test=row["created_at"]
        )

    def toUsers_test(self,rows) -> List[User_test]:
        return [self.toUser_test(row) for row in rows]
