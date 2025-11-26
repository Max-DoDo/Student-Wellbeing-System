
from dataclasses import dataclass

@dataclass
class WellbingSurveys:
    survey_id:int
    student_id:int
    week_number:int
    stress_level:int
    hours_slept:int
    survey_date:str
    