
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from base.tools.mytools import MyTools

@dataclass
class Wellbeing_Survey:
    survey_id:Optional[int] = -1
    student_id:Optional[int] = -1
    week_number:Optional[int] = -1
    stress_level:Optional[int] = -1
    hours_slept:Optional[int] = -1
    survey_date:Optional[str] = -1

    def __post_init__(self):
        if self.survey_date == None:
            self.survey_date = MyTools().getFormattedDate()
        