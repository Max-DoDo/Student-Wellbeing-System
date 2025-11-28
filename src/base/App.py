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
import sys

class App:
    def __init__(self):

        self.main() 

    def main(self) -> None:
        Log.isFileLogging(True)
        self.configure_DataBase();
        Log.debug(sys.path)
        self.test();
    
    def test(self):
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
        Log.success("Success Configure DataBase Path")

if __name__ == "__main__":
    App()
    app.run(debug=True, use_reloader=False)
