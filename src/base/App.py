import os
from entity.user import User
from repository.user_repo import User_Repo
from repository.student_repo import Student_Repo
from repository.base_repo import Base_Repo
from entity.person import Person

class App:
    def __init__(self):
        self.configure_DataBase();
        self.main() 

    def main(self) -> None:

        self.test();
    
    def test(self):
        user = User(username="aaa",id=121,name="Max Wang", gender="M",email="hahaha@hahah.haha",password="123123",
                    role_id="111",)
        # print(user)
        userr = User_Repo();
        # print(userr.getAllUser())
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
