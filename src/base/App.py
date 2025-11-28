import os
from entity.student import Student
from tools.log import Log
from tools.mytools import MyTools
from repository.attendance_repo import Attendance_Repo
from entity.user import User
from repository.user_repo import User_Repo
from repository.student_repo import Student_Repo
from repository.base_repo import Base_Repo
from services.student_service import Student_Service
from entity.person import Person
from ui.app import app

class App:
    def __init__(self):
        self.configure_DataBase();
        self.main() 

    def main(self) -> None:
        # student = Student(name="Max Wang",id=234234)
        # Student_Service().add(student)
        self.test();
    
    def test(self):
        
        Log.isFileLogging(True)
        # Log.info("aaa")
        # Log.success("Success")
        # Log.warn("Warn")
        # Log.debug("debug")
        # Log.error("error")
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
    App()
    Log.success("Success launch backend")
    app.run(debug=True)
    Log.success("Success launch UI")
