from typing import List, Optional
from base.repository.base_repo import Base_Repo
from entity.student import Student

class Student_Repo(Base_Repo):

    def getStudent(self, id: int) -> Optional[Student]:
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return Student(id=row["student_id"], 
                           first_name=row["first_name"], 
                           last_name=row["last_name"],
                           )
        return None

    def getAllStudent(self) -> List[Student]:
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        if rows:
            rows = self.cursor.fetchall()
            return self.rows_to_student(rows)
        return None
    
    def row_to_student(self, row) -> Student:
        return Student(
            id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            personal_tutor_email=row["personal_tutor_email"],
            emergency_contact_name=row["emergency_contact_name"],
            emergency_contact_phone=row["emergency_contact_phone"]
        )
    
    def rows_to_student(self,rows) -> List[Student]:
        return [self.row_to_student(row) for row in rows]