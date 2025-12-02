import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from typing import List, Optional
from test.base_test.entity_test.attendance_test import Attendance_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

class Attendance_Repo_test(Base_Repo_test):
    
    
    def getAttendance(self,id=int) -> Optional[Attendance_test]:
        query = "SELECT * FROM attendance WHERE attendance_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toAttendance(row)
        return None
    
    def getAttendancesByStudentID(self, studentid = int) -> List[Optional[Attendance_test]]:
        query = "SELECT * FROM attendance WHERE student_id = ?"
        self.cursor.execute(query,(studentid))
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances(rows)
        return None
    
    def getAllAttendance(self) -> List[Attendance_test]:
        query = "SELECT * FROM attendance"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toAttendances(rows)
        return None

    def toAttendance(self,row) -> Attendance_test:
        return Attendance_test(
            attendance_id=row["attendance_id"],
            student_id=row["student_id"],
            week_number=row["week_number"],
            is_present=bool(row["is_present"]),
            is_late=bool(row["is_late"])
        )

    def toAttendances(self,rows) -> List[Attendance_test]:
        return [self.toAttendance(row) for row in rows]