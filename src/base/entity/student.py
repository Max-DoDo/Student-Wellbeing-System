
from dataclasses import dataclass
from entity.person import Person
from typing import Optional

@dataclass
class Student(Person):
    personal_tutor_email: Optional[str] = None
    emergency_contact_name:Optional[str] = None
    emergency_contact_phone:Optional[str] = None