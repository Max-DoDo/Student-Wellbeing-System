from dataclasses import dataclass
from tools.mytools import MyTools

@dataclasss
class Assessment_test:
    assessment_id_test:int
    student_id_test:int
    assignment_name_test:str
    grade_test:int
    submitted_on_time_test:str

    def __post_init__(self):
        super().__post_init__()
        if self.submitted_on_time_test == None:
            self.submitted_on_time_test = MyTools.getFormattedDate();