from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Person(ABC):

    id: int
    name: str
    gender: str
    first_name:str
    last_name:str
    email:str