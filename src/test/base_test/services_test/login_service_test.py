from repository_test.user_repo_test import User_Repo_test
from typing import List
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".." ))
sys.path.insert(0, SRC_PATH)

from base.tools.log import Log

class Login_Service_test:

    ''' 
    return value:  bool -> 
    - True for correct password. 
    - False for wrong password or username or did not find the user
    '''
    def login_user_test(self, username_test: str, password_test: str):
        user_repo_test = User_Repo_test()
        user_test = user_repo_test.getUserByUserName_test(username_test)
        
        if user_test is None:
            Log.warn("User is not fonded")
            return [False,-1]

        if user_test.password_test == password_test:
            Log.success("User Login with username: ", user_test.username_test)
            return [True, user_test.role_id_test]
        else:
            Log.warn("User Login failed with username: ", user_test.username_test, " privided")
            return [False,-1]
