import os
from repository.student_repo import Student_Repo
from repository.baserepo import BaseRepo
from entity.person import Person

class App:
    def __init__(self):
        self.configure_DataBase();
        self.main() 


    def main(self) -> None:

        # current_dir = os.path.dirname(os.path.abspath(__file__))    
        # db_folder = os.path.abspath(os.path.join(current_dir, "..", "..", "database"))     
        # self.db_path = os.path.join(db_folder, "university_wellbeing.db") 
        # repo = Student_Repo(self.db_path)

        # studentsById = repo.getStudent(10)
        # students = repo.getAllStudent()
        # print(studentsById)
        # print(students)

        self.test();
    
    def test(self):
        studentrp = Student_Repo();
        print(studentrp.getStudent(10));

        pass

    def configure_DataBase(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.abspath(os.path.join(
            current_dir,
            "..",   # base → src
            "..",   # src → root
            "database",
            "university_wellbeing.db"
        ))

        # print("[DEBUG] PATH =", db_path)
        # print("[DEBUG] exists =", os.path.exists(db_path))

        BaseRepo.set_db_path(db_path)

if __name__ == "__main__":
    app = App()
