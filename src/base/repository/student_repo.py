from typing import List, Optional
from repository.baserepo import BaseRepo
from entity.student import Student

class Student_Repo(BaseRepo):

    def getStudent(self, id: int) -> Optional[Student]:
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (id,))
        row = self.cursor.fetchone()

        if row:
            # print(row["student_id"])
            return Student(id=row["student_id"], first_name=row["first_name"], last_name=row["last_name"])
        return None

    def getAllStudent(self) -> List[Student]:
        """
        Retrieves all users and maps them to Student objects.
        """
        query = "SELECT * FROM students"
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results