from dataclasses import dataclass

@dataclass
class Assessment:
    assessment_id:int
    student_id:int
    assignment_name:str
    grade:int
    submitted_on_time:str
    