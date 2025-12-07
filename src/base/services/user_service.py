from base.entity.wellbeing_survey import Wellbeing_Survey
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo


class user_service:

    def __init__(self, wellbeing_survey_repo: Wellbeing_Survey_Repo = None):
        self.wellbeing_survey_repo = wellbeing_survey_repo if wellbeing_survey_repo else Wellbeing_Survey_Repo()

    def addWellbeingSurvey(self, survey: Wellbeing_Survey) -> int:
        return self.wellbeing_survey_repo.addWellbeingSurvey(survey)

