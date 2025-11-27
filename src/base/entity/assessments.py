from dataclasses import dataclass
from datetime import datetime

@dataclass
class Assessment:
    assessment_id:int
    student_id:int
    assignment_name:str
    grade:int
    submitted_on_time:str

    def __post_init__(self):
        super().__post_init__()
        if self.submitted_on_time == None:
            self.submitted_on_time = datetime.now().strftime("%Y-%m-%d")
        