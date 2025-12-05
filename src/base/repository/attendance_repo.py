from typing import List, Optional
from base.entity.attendance import Attendance
from base.repository.base_repo import Base_Repo

class Attendance_Repo(Base_Repo):
    
    
    def getAttendance(self,id=int) -> Optional[Attendance]:
        query = "SELECT * FROM attendance WHERE attendance_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toAttendance(row)
        return None
    
    def getAttendancesByStudentID(self, studentid = int) -> List[Optional[Attendance]]:
        query = "SELECT * FROM attendance WHERE student_id = ?"
        self.cursor.execute(query,(studentid))
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances(rows)
        return None
    
    def getAllAttendance(self) -> List[Attendance]:
        query = "SELECT * FROM attendance"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances(rows)
        return None

    def toAttendance(self,row) -> Attendance:
        return Attendance(
            attendance_id=row["attendance_id"],
            student_id=row["student_id"],
            week_number=row["week_number"],
            is_present=bool(row["is_present"]),
            is_late=bool(row["is_late"])
        )

    def toAttendances(self,rows) -> List[Attendance]:
        return [self.toAttendance(row) for row in rows]