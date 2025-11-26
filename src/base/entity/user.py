from dataclasses import dataclass
from entity.person import Person
from datetime import datetime
@dataclass
class user(Person):

    user_id:int
    user_name:str
    password:str
    first_name:str
    last_name:str
    email:str
    role_id:int
    is_active:bool
    created_at:str