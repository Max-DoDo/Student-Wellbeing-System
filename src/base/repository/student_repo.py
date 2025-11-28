from typing import List, Optional
from tools.log import Log
from repository.base_repo import Base_Repo
from entity.student import Student

class Student_Repo(Base_Repo):

    def getStudent(self, id: int) -> Optional[Student]:
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row:
            return self.toStudent(row)
        return None

    def getAllStudent(self) -> List[Student]:
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if rows:
            return self.toStudents(rows)
        return None
    
    def addStudent(self, student: Student) -> int:
        required_fields = [student.first_name, 
                           student.last_name,
                           student.email
                           ]
        if any(not field for field in required_fields):
            Log.error("Missing required student fields When adding Student into database")
            raise ValueError("Missing required student fields (first_name, last_name, email, personal_tutor_email).")
        
        if student.id == -1:
             # auto generate student_id
            Log.info("Added Student: blank id filed. Auto generated")
            query = """
                INSERT INTO students 
                (first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, ?, ?, ?)
                """
            values = (
                student.first_name,
                student.last_name,
                student.email,
                student.personal_tutor_email,
                student.emergency_contact_name,
                student.emergency_contact_phone
            )
        else:
            query = """
                INSERT INTO students 
                (student_id, first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
            values = (
                student.id,
                student.first_name,
                student.last_name,
                student.email,
                student.personal_tutor_email,
                student.emergency_contact_name,
                student.emergency_contact_phone
            )

        self.cursor.execute(query, values)
        self.conn.commit()
        Log.info("Added Student:" ,student.name," ID:", student.id, " to database")
        return student.id if student.id is not None else self.cursor.lastrowid
    
    def updateStudent(self, new_data: Student) -> bool:

        id = new_data.id
        field_map = {
            "first_name": new_data.first_name,
            "last_name": new_data.last_name,
            "email": new_data.email,
            "personal_tutor_email": new_data.personal_tutor_email,
            "emergency_contact_name": new_data.emergency_contact_name,
            "emergency_contact_phone": new_data.emergency_contact_phone
        }

        updates = {field: value for field, value in field_map.items() if value is not None}

        if not updates:
            Log.warn("No data has update")
            raise ValueError("No fields to update — all provided fields are None.")
        
        set_clause = ", ".join(f"{field} = ?" for field in updates.keys())
        values = list(updates.values())
        values.append(id)
        query = f"""
        UPDATE students
        SET {set_clause}
        WHERE student_id = ?
        """
        self.cursor.execute(query, values)
        self.conn.commit()
        Log.info("Updated Student ID: ", id," with data: ", updates)
        return self.cursor.rowcount > 0

    def deleteStudent(self, student: Student) -> bool:
        if student is None:
            Log.warn("deleteStudent failed: student is None")
            return False
        
        query = "DELETE FROM students WHERE id = ?"
        self.cursor.execute(query, (student.id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            Log.success(f"Student deleted successfully: ID={student.id}")
            return True
        else:
            Log.warn(f"No student found with ID={student.id} failed to delete")
            return False


        

    def toStudent(self, row) -> Student:
        return Student(
            id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            personal_tutor_email=row["personal_tutor_email"],
            emergency_contact_name=row["emergency_contact_name"],
            emergency_contact_phone=row["emergency_contact_phone"]
        )
    
    def toStudents(self,rows) -> List[Student]:
        return [self.toStudent(row) for row in rows]