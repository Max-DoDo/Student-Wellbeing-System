from dataclasses import dataclass
from typing import Optional

@dataclass
class Attendance_test:
    attendance_id_test:Optional[int] = None
    student_id_test:Optional[int] = None
    week_number_test:Optional[int] = None
    is_present_test:Optional[bool] = None
    is_late_test:Optional[bool] = None
