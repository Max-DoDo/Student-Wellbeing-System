from typing import List, Optional
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..","..",".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from test.base_test.repository_test.base_repo_test import Base_Repo_test

class Wellbeing_Survey_Repo_test(Base_Repo_test):
    
    def getWellBeingSurvey(self, id=int) -> Optional[Wellbeing_Survey_test]:
        query = "SELECT * FROM wellbeing_surveys WHERE survey_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toWellBeingSurvey(row)
        return None

    def getWellBeingSurveys(self) -> List[Wellbeing_Survey_test]:
        query = "SELECT * FROM wellbeing_surveys"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toWellBeingSurveys(rows)
        return None
    
    def getWellBeingSurveysByStudentID(self, student_id = int) -> List[Optional[Wellbeing_Survey_test]]:
        query = "SELECT * FROM wellbeing_surveys WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        rows = self.cursor.fetchall()
        if rows:
            return self.toWellBeingSurveys(rows)
        return None

    def toWellBeingSurvey(self, row) -> Wellbeing_Survey_test:
        return Wellbeing_Survey_test(
            survey_id=row["survey_id"],
            student_id=row["student_id"],
            week_number=row["week_number"],
            stress_level=row["stress_level"],
            hours_slept=row["hours_slept"],
            survey_date=row["survey_date"]
        )

    def toWellBeingSurveys(self, rows) -> List[Wellbeing_Survey_test]:
        return [self.toWellBeingSurvey(row) for row in rows]