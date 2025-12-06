
from dataclasses import dataclass
from entity_test.person_test import Person_test
from typing import Optional

@dataclass
class Student_test(Person_test):
    personal_tutor_email: Optional[str] = ""
    emergency_contact_name:Optional[str] = ""
    emergency_contact_phone:Optional[str] = ""