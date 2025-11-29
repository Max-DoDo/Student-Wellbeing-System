from typing import List, Optional
from entity.wellbeing_survey import Wellbeing_Survey
from repository.base_repo import Base_Repo

class Wellbeing_Survey_Repo(Base_Repo):
    
    def getWellBeingSurvey(self, id=int) -> Optional[Wellbeing_Survey]:
        query = "SELECT * FROM wellbeing_surveys WHERE survey_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toWellBeingSurvey(row)
        return None

    def getWellBeingSurveys(self) -> List[Wellbeing_Survey]:
        query = "SELECT * FROM wellbeing_surveys"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toWellBeingSurveys(rows)
        return None
    
    def getWellBeingSurveysByStudentID(self, student_id = int) -> List[Optional[Wellbeing_Survey]]:
        query = "SELECT * FROM wellbeing_surveys WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        rows = self.cursor.fetchall()
        if rows:
            return self.toWellBeingSurveys(rows)
        return None

    def toWellBeingSurvey(self, row) -> Wellbeing_Survey:
        return Wellbeing_Survey(
            survey_id=row["survey_id"],
            student_id=row["student_id"],
            week_number=row["week_number"],
            stress_level=row["stress_level"],
            hours_slept=row["hours_slept"],
            survey_date=row["survey_date"]
        )

    def toWellBeingSurveys(self, rows) -> List[Wellbeing_Survey]:
        return [self.toWellBeingSurvey(row) for row in rows]