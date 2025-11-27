
from dataclasses import dataclass

@dataclass
class Attendance:
    attendance_id:int
    student_id:int
    week_number:int
    is_present:bool
    is_late:bool
    