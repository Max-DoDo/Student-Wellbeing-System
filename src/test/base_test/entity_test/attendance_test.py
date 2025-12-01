from dataclasses import dataclass
from typing import Optional

@dataclass
class Attendance_test:
    attendance_id:Optional[int] = None
    student_id:Optional[int] = None
    week_numbe:Optional[int] = None
    is_present:Optional[bool] = None
    is_late:Optional[bool] = None
