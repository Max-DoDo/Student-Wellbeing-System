from repository.user_repo import User_Repo
from tools.log import Log

class Login_Service:
    ''' return value:  bool -> True for correct password. False for wrong password or username'''
    def login_user(username: str, password: str) -> bool:
        user_repo = User_Repo();
        user = user_repo.getUserByUserName(username);
        
        if user is None:
            Log.warn("User is not fonded")
            return False

        if user.password == password:
            return True
        else:
            return False
        pass