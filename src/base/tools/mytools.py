
from datetime import datetime
import sys

class MyTools:

    def __init__(self):
        pass
    
    def getFormattedDate(self):
        return datetime.now().strftime("%Y-%m-%d")
