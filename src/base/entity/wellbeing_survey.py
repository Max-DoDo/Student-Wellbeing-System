
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Wellbeing_Survey:
    survey_id:int
    student_id:int
    week_number:int
    stress_level:int
    hours_slept:int
    survey_date:str

    def __post_init__(self):
        super().__post_init__()
        if self.survey_date == None:
            self.survey_date = datetime.now().strftime("%Y-%m-%d")
        