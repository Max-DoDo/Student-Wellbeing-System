from base.repository.user_repo import User_Repo
from typing import List
from base.tools.log import Log

class Login_Service:

    def __init__(self, user_repo: User_Repo = None):
        self.user_repo = user_repo if user_repo else User_Repo()

    def login_user(self, username: str, password: str):
        user = self.user_repo.getUserByUserName(username)
        
        if user is None:
            Log.warn("User is not fonded")
            return [False,-1]

        if user.password == password:
            Log.success("User Login with username: ",user.username)
            return [True,user.role_id]
        else:
            Log.warn("User Login failed with username: ", user.username, " privided")
            return [False,-1]


        
    
