from typing import List
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.log import Log
from test.base_test.repository_test.user_repo_test import User_Repo_test

class Login_Service_test:

    ''' 
    return value:  bool -> 
    - True for correct password. 
    - False for wrong password or username or did not find the user
    '''
    def login_user(self, username: str, password: str):
        user_repo = User_Repo_test()
        user = user_repo.getUserByUserName(username)
        
        if user is None:
            Log.warn("User is not fonded")
            return [False,-1]

        if user.password == password:
            Log.success("User Login with username: ",user.username)
            return [True,user.role_id]
        else:
            Log.warn("User Login failed with username: ", user.username, " privided")
            return [False,-1]
