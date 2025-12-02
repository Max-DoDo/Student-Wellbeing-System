import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from typing import List, Optional
from test.base_test.entity_test.assessments_test import Assessment_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

class Assessment_Repo_test(Base_Repo_test):
    
    def getAssessment(self,id=int) -> Optional[Assessment_test]:
        query = "SELECT * FROM assessments WHERE assessment_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toAssessment(row)
        return None

    def getAssessments(self) -> Optional[List[Assessment_test]]:
        query = "SELECT * FROM assessments"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toAssessments(rows)
        return None
    
    def getAssessmentsByStudentID(self, student_id = int) -> Optional[List[Assessment_test]]:
        query = "SELECT * FROM assessments WHERE student_id = ?"
        self.cursor.execute(query, (id,))
        rows = self.cursor.fetchall()
        if rows:
            return self.toAssessment(rows)
        return None
    
    def toAssessment(self, row)-> Assessment_test:
        return Assessment_test(
            assessment_id=row["assessment_id"],
            student_id=row["student_id"],
            assignment_name=row["assignment_name"],
            grade=row["grade"],
            submitted_on_time=row["submitted_on_time"]
        )

    def toAssessments(self, rows) -> List[Assessment_test]:
        return [self.toAssessment(row) for row in rows]
