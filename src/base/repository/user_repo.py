from typing import List, Optional
from tools.log import Log
from entity.user import User
from repository.base_repo import Base_Repo

class User_Repo(Base_Repo):

    def getUser(self,id : int) -> Optional[User]:
        query = "SELECT * FROM users WHERE users_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toUser(row)
        return None
    
    def getUserByUserName(self, username : str) -> Optional[User]:
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

        

    def toUser(self,row) -> User:
        return User(
            id=row["users_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            username=row["username"],
            password=row["password"],
            role_id=row["role_id"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            is_subscribed=row["is_subscribed"],
            received_report_at=row["received_report_at"]
        )

    def toUsers(self,rows) -> List[User]:
        return [self.toUser(row) for row in rows]


