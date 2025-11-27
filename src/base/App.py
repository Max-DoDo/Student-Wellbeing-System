import os
from repository.student_repo import Student_Repo
from base.repository.base_repo import Base_Repo
from entity.person import Person

class App:
    def __init__(self):
        self.configure_DataBase();
        self.main() 

    def main(self) -> None:

        self.test();
    
    def test(self):
        studentrp = Student_Repo();
        print(studentrp.getAllStudent());
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
        Base_Repo.set_db_path(db_path)

if __name__ == "__main__":
    app = App()
