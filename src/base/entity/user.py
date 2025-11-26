from dataclasses import dataclass
from entity.person import Person
from datetime import datetime
@dataclass
class user(Person):

    password:str
    role_id:int
    is_active:bool
    created_at:str