from typing import List, Optional
from repository.baserepo import BaseRepo
from entity.student import Student

class Student_Repo(BaseRepo):

    def getStudent(self, id: int) -> str:
        
        print(f"Fetching name for student ID: {id}")
        query = "SELECT * FROM students WHERE student_id = ?"
        
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchall()
        print(result)

    def getAllStudent(self) -> List[Student]:
        """
        Retrieves all users and maps them to Student objects.
        """
        query = "SELECT * FROM students"
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results