from dataclasses import dataclass
from typing import Optional
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.mytools import MyTools
from test.base_test.entity_test.person_test import Person_test


@dataclass
class User_test(Person_test):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        # super().__post_init__()
        if self.created_at == None:
            self.created_at = MyTools.getFormattedDate()
