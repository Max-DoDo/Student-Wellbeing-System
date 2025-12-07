from typing import List, Optional
from base.entity.assessments import Assessment
from base.repository.base_repo import Base_Repo

class Assessment_Repo(Base_Repo):
    
    def getAssessment(self,id=int) -> Optional[Assessment]:
        query = "SELECT * FROM assessments WHERE assessment_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toAssessment(row)
        return None

    def getAssessments(self) -> Optional[List[Assessment]]:
        query = "SELECT * FROM assessments"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toAssessments(rows)
        return None
    
    def getAssessmentsByStudentID(self, id = int) -> Optional[List[Assessment]]:
        query = "SELECT * FROM assessments WHERE student_id = ?"
        self.cursor.execute(query, (id,))
        rows = self.cursor.fetchall()
        if rows:
            return self.toAssessments(rows)
        return None

    def toAssessment(self, row)-> Assessment:
        return Assessment(
            assessment_id=row["assessment_id"],
            student_id=row["student_id"],
            assignment_name=row["assignment_name"],
            grade=row["grade"],
            submitted_on_time=row["submitted_on_time"]
        )

    def toAssessments(self, rows) -> List[Assessment]:
        return [self.toAssessment(row) for row in rows]

    def addAssessment(self, assessment: Assessment) -> int:
        if (assessment.student_id is None or assessment.assignment_name is None or assessment.grade is None or
            assessment.submitted_on_time is None or assessment.submitted_on_time == ""):
            raise ValueError("Missing required assessment fields (student_id, assignment_name, grade, submitted_on_time).")

        if assessment.assessment_id is None:
            query = """
                INSERT INTO assessments
                (student_id, assignment_name, grade, submitted_on_time)
                VALUES (?, ?, ?, ?)
                """
            values = (
                assessment.student_id,
                assessment.assignment_name,
                assessment.grade,
                assessment.submitted_on_time
            )
        else:
            query = """
                INSERT INTO assessments
                (assessment_id, student_id, assignment_name, grade, submitted_on_time)
                VALUES (?, ?, ?, ?, ?)
                """
            values = (
                assessment.assessment_id,
                assessment.student_id,
                assessment.assignment_name,
                assessment.grade,
                assessment.submitted_on_time
            )

        self.cursor.execute(query, values)
        self.conn.commit()
        return assessment.assessment_id if assessment.assessment_id is not None else self.cursor.lastrowid

    def deleteAssessmentsByStudentID(self, sid):
        query = "DELETE FROM assessments WHERE student_id = ?"
        self.cursor.execute(query, (sid,))
        self.conn.commit()
