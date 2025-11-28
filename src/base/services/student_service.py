from entity.student import Student
from repository.student_repo import Student_Repo

class Student_Service:

    def getAllStudent(self) -> list[Student]:
        student_repo = Student_Repo()
        return student_repo.getAllStudent()