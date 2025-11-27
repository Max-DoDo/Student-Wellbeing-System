
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tools.mytools import MyTools

@dataclass
class Wellbeing_Survey:
    survey_id:Optional[int] = None
    student_id:Optional[int] = None
    week_number:Optional[int] = None
    stress_level:Optional[int] = None
    hours_slept:Optional[int] = None
    survey_date:Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.survey_date == None:
            self.survey_date = MyTools.getFormattedDate();
        