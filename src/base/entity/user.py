from dataclasses import dataclass
from typing import Optional
from base.tools.mytools import MyTools
from base.entity.person import Person


@dataclass
class User(Person):
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    is_subscribed: Optional[bool] = True
    received_report_at: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.created_at == None:
            self.created_at = MyTools.getFormattedDate()

