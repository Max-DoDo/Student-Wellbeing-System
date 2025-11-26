
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Person(ABC):

    id: str
    name: str
    gender: str