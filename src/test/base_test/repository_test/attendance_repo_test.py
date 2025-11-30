from typing import List, Optional
from entity_test.attendance_test import Attendance_test
from repository_test.base_repo_test import Base_Repo_test

class Attendance_Repo_test(Base_Repo_test):
    
    
    def getAttendance_test(self, id_test=int) -> Optional[Attendance_test]:
        query = "SELECT * FROM attendance WHERE attendance_id = ?"
        self.cursor.execute(query, (id_test,))
        row = self.cursor.fetchone()
        if row:
            return self.toAttendance_test(row)
        return None
    
    def getAttendancesByStudentID_test(self, studentid_test = int) -> List[Optional[Attendance_test]]:
        query = "SELECT * FROM attendance WHERE student_id = ?"
        self.cursor.execute(query,(studentid_test))
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances_test(rows)
        return None
    
    def getAllAttendance_test(self) -> List[Attendance_test]:
        query = "SELECT * FROM attendance"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances_test(rows)
        return None

    def toAttendance_test(self,row) -> Attendance_test:
        return Attendance_test(
            attendance_id_test=row["attendance_id"],
            student_id_test=row["student_id"],
            week_number_test=row["week_number"],
            is_present_test=bool(row["is_present"]),
            is_late_test=bool(row["is_late"])
        )

    def toAttendances_test(self,rows) -> List[Attendance_test]:
        return [self.toAttendance_test(row) for row in rows]
