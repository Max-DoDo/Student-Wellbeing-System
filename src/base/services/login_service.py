from repository.user_repo import User_Repo
from typing import List
from tools.log import Log

class Login_Service:

    ''' 
    return value:  bool -> 
    - True for correct password. 
    - False for wrong password or username or did not find the user
    '''
    def login_user(username: str, password: str) -> List[bool,int]:
        user_repo = User_Repo()
        user = user_repo.getUserByUserName(username)
        
        if user is None:
            Log.warn("User is not fonded")
            return False

        if user.password == password:
            Log.success("User Login with username: ",user.username)
            return [True,user.role_id]
        else:
            Log.warn("User Login failed with username: ", user.username, " privided")
            return False


        
    
