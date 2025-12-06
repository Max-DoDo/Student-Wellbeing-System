
from dataclasses import dataclass
from entity.person import Person
from typing import Optional

@dataclass
class Student(Person):
    personal_tutor_email: Optional[str] = ""
    emergency_contact_name:Optional[str] = ""
    emergency_contact_phone:Optional[str] = ""

    def __post_init__(self):
        super().__post_init__()