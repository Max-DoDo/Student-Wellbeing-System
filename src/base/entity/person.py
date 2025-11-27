from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class Person(ABC):

    id: int
    name: Optional[str] = None
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    gender: Optional[str] = None
    email:Optional[str] = None

    def __post_init__(self):

        if not (self.first_name or self.last_name or self.name):
            raise ValueError("Person requires at least a name!")
        
        if self.name is None:
            self.name = f"{self.first_name} {self.last_name}"


        if self.name and (not self.first_name or not self.last_name):
            parts = self.name.split()
            self.first_name = parts[0]
            self.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""