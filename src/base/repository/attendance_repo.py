from typing import List, Optional
from entity.attendance import Attendance
from repository.base_repo import Base_Repo

class Attendance_Repo(Base_Repo):
    
    
    def getAttendence(self,id=int) -> Attendance:
        query = "SELECT * FROM attendance WHERE users_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toUser(row)
        return None