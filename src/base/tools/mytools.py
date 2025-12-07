
from datetime import datetime
import sys

class MyTools:

    def __init__(self):
        pass
    
    @staticmethod
    def getFormattedDate():
        return datetime.now().strftime("%Y-%m-%d")
