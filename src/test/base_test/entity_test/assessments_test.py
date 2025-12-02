import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.mytools import MyTools
from dataclasses import dataclass

@dataclass
class Assessment_test:
    assessment_id:int
    student_id:int
    assignment_name:str
    grade:int
    submitted_on_time:str

    def __post_init__(self):
        # super().__post_init__()
        if self.submitted_on_time == None:
            self.submitted_on_time = MyTools.getFormattedDate();
