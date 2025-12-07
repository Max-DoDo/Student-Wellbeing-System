from base.entity.wellbeing_survey import Wellbeing_Survey
from base.entity.attendance import Attendance
from base.entity.assessments import Assessment
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
from base.repository.attendance_repo import Attendance_Repo
from base.repository.assessment_repo import Assessment_Repo


class user_service:

    def __init__(self, wellbeing_survey_repo: Wellbeing_Survey_Repo = None, attendance_repo: Attendance_Repo = None, assessment_repo: Assessment_Repo = None):
        self.wellbeing_survey_repo = wellbeing_survey_repo if wellbeing_survey_repo else Wellbeing_Survey_Repo()
        self.attendance_repo = attendance_repo if attendance_repo else Attendance_Repo()
        self.assessment_repo = assessment_repo if assessment_repo else Assessment_Repo()

    def addWellbeingSurvey(self, survey: Wellbeing_Survey) -> int:
        return self.wellbeing_survey_repo.addWellbeingSurvey(survey)

    def addAttendance(self, attendance: Attendance) -> int:
        return self.attendance_repo.addAttendance(attendance)

    def addAssessment(self, assessment: Assessment) -> int:
        return self.assessment_repo.addAssessment(assessment)

