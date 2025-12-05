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
    
    def getAssessmentsByStudentID(self, student_id = int) -> Optional[List[Assessment]]:
        query = "SELECT * FROM assessments WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
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
