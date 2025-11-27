
from dataclasses import dataclass
from entity.person import Person

@dataclass
class Student(Person):
    personal_tutor_email:str
    emergency_contact_name:str
    emergency_contact_phone:str