from typing import List, Optional
from entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from repository_test.base_repo_test import Base_Repo_test

class Wellbeing_Survey_Repo_test(Base_Repo_test):
    
    def getWellBeingSurvey_test(self, id_test=int) -> Optional[Wellbeing_Survey_test]:
        query = "SELECT * FROM wellbeing_surveys WHERE survey_id = ?"
        self.cursor_test.execute(query, (id_test,))
        row = self.cursor_test.fetchone()
        if row:
            return self.toWellBeingSurvey_test(row)
        return None

    def getWellBeingSurveys_test(self) -> List[Wellbeing_Survey_test]:
        query = "SELECT * FROM wellbeing_surveys"
        self.cursor_test.execute(query)
        rows = self.cursor_test.fetchall()
        if rows:
            return self.toWellBeingSurveys_test(rows)
        return None
    
    def getWellBeingSurveysByStudentID_test(self, student_id_test = int) -> List[Optional[Wellbeing_Survey_test]]:
        query = "SELECT * FROM wellbeing_surveys WHERE student_id = ?"
        self.cursor_test.execute(query, (student_id_test,))
        rows = self.cursor_test.fetchall()
        if rows:
            return self.toWellBeingSurveys_test(rows)
        return None

    def toWellBeingSurvey_test(self, row) -> Wellbeing_Survey_test:
        return Wellbeing_Survey_test(
            survey_id_test=row["survey_id"],
            student_id_test=row["student_id"],
            week_number_test=row["week_number"],
            stress_level_test=row["stress_level"],
            hours_slept_test=row["hours_slept"],
            survey_date_test=row["survey_date"]
        )

    def toWellBeingSurveys_test(self, rows) -> List[Wellbeing_Survey_test]:
        return [self.toWellBeingSurvey_test(row) for row in rows]
