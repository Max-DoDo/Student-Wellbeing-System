
from dataclasses import dataclass
from base.entity.person import Person
from typing import Optional

@dataclass
class Student(Person):
    personal_tutor_email: Optional[str] = ""
    emergency_contact_name:Optional[str] = ""
    emergency_contact_phone:Optional[str] = ""