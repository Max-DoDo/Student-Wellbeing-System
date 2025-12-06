from dataclasses import dataclass
from base.tools.mytools import MyTools

@dataclass
class Assessment:
    assessment_id:int
    student_id:int
    assignment_name:str
    grade:int
    submitted_on_time:str

    def __post_init__(self):
        if self.submitted_on_time == None:
            self.submitted_on_time = MyTools.getFormattedDate();
        
