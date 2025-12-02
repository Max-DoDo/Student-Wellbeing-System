from dataclasses import dataclass
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..","..",".."))
sys.path.insert(0, SRC_PATH)
from test.base_test.entity_test.person_test import Person_test
from typing import Optional

@dataclass
class Student_test(Person_test):
    personal_tutor_email: Optional[str] = ""
    emergency_contact_name:Optional[str] = ""
    emergency_contact_phone:Optional[str] = ""