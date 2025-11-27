from repository.baserepo import BaseRepo
from src.base.entity.student import Student
class Student_Repo(BaseRepo):

    def getStudentName(self, id) -> str:
        pass;

    def getAllStudent(self) -> Student:
        pass;