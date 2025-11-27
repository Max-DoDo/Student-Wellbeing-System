from dataclasses import dataclass
from typing import Optional
from entity.person import Person
from datetime import datetime

@dataclass
class User(Person):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.created_at == None:
            self.created_at = datetime.now().strftime("%Y-%m-%d")
            print(self.created_at)
