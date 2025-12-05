from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from tools.log import Log

@dataclass
class Person(ABC):

    id: Optional[int] = -1
    name: Optional[str] = ""
    first_name:Optional[str] = ""
    last_name:Optional[str] = ""
    gender: Optional[str] = ""
    email:Optional[str] = ""

    def __post_init__(self):

        if not (self.first_name or self.last_name or self.name):
            Log.warn("A no name person object has been created with id", self.id)
            return
        
        if self.name is None:
            self.name = f"{self.first_name} {self.last_name}"


        if self.name and (not self.first_name or not self.last_name):
            parts = self.name.split()
            self.first_name = parts[0]
            self.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""