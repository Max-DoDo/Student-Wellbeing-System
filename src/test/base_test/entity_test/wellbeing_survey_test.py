from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.mytools import MyTools

@dataclass
class Wellbeing_Survey_test:
    survey_id:Optional[int] = -1
    student_id:Optional[int] = -1
    week_number:Optional[int] = -1
    stress_level:Optional[int] = -1
    hours_slept:Optional[int] = -1
    survey_date:Optional[str] = -1

    def __post_init__(self):
        if self.survey_date == None:
            self.survey_date = MyTools.getFormattedDate();
