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
        self.cursor.execute(query,(studentid,))
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

    def addAttendance(self, attendance: Attendance) -> int:
        if attendance.student_id is None or attendance.week_number is None or attendance.is_present is None or attendance.is_late is None:
            raise ValueError("Missing required attendance fields (student_id, week_number, is_present, is_late).")

        if attendance.attendance_id is None:
            query = """
                INSERT INTO attendance
                (student_id, week_number, is_present, is_late)
                VALUES (?, ?, ?, ?)
                """
            values = (
                attendance.student_id,
                attendance.week_number,
                int(attendance.is_present),
                int(attendance.is_late)
            )
        else:
            query = """
                INSERT INTO attendance
                (attendance_id, student_id, week_number, is_present, is_late)
                VALUES (?, ?, ?, ?, ?)
                """
            values = (
                attendance.attendance_id,
                attendance.student_id,
                attendance.week_number,
                int(attendance.is_present),
                int(attendance.is_late)
            )

        self.cursor.execute(query, values)
        self.conn.commit()
        return attendance.attendance_id if attendance.attendance_id is not None else self.cursor.lastrowid

    def deleteAttendanceByStudentID(self, sid):
        query = "DELETE FROM attendance WHERE student_id = ?"
        self.cursor.execute(query, (sid,))
        self.conn.commit()