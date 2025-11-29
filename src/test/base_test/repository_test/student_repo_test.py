from typing import List, Optional
from tools.log import Log
from repository.base_repo_test import Base_Repo_test
from entity.student_test import Student_test

class Student_Repo_test(Base_Repo_test):

    def getStudent_test(self, id_test: int) -> Optional[Student_test]:
        query = "SELECT * FROM students WHERE student_id = ?"
        self.cursor_test.execute(query, (id_test,))
        row = self.cursor_test.fetchone()
        if row:
            return self.toStudent_test(row)
        return None

    def getAllStudent_test(self) -> List[Student_test]:
        query = "SELECT * FROM students"
        self.cursor_test.execute(query)
        rows = self.cursor_test.fetchall()
        if rows:
            return self.toStudents_test(rows)
        return None
    
    def addStudent_test(self, student_test: Student_test) -> int:
        required_fields_test = [student_test.first_name_test, 
                                student_test.last_name_test,
                                student_test.email_test
                                ]
        if any(not field for field in required_fields_test):
            Log.error("Missing required student fields When adding Student into database")
            raise ValueError("Missing required student fields (first_name, last_name, email, personal_tutor_email).")
        
        if student_test.id_test == -1:
             # auto generate student_id
            Log.info("Added Student: blank id filed. Auto generated")
            query = """
                INSERT INTO students 
                (first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, ?, ?, ?)
                """
            values_test = (
                student_test.first_name_test,
                student_test.last_name_test,
                student_test.email_test,
                student_test.personal_tutor_email_test,
                student_test.emergency_contact_name_test,
                student_test.emergency_contact_phone_test
            )
        else:
            query = """
                INSERT INTO students 
                (student_id, first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
            values_test = (
                student_test.id_test,
                student_test.first_name_test,
                student_test.last_name_test,
                student_test.email_test,
                student_test.personal_tutor_email_test,
                student_test.emergency_contact_name_test,
                student_test.emergency_contact_phone_test
            )

        self.cursor_test.execute(query, values_test)
        self.conn_test.commit()
        Log.info("Added Student:" ,student_test.name_test," ID:", student_test.id_test, " to database")
        return student_test.id_test if student_test.id_test is not None else self.cursor_test.lastrowid
    
    def updateStudent_test(self, new_data_test: Student_test) -> bool:

        id_test = new_data_test.id_test
        field_map_test = {
            "first_name": new_data_test.first_name_test,
            "last_name": new_data_test.last_name_test,
            "email": new_data_test.email_test,
            "personal_tutor_email": new_data_test.personal_tutor_email_test,
            "emergency_contact_name": new_data_test.emergency_contact_name_test,
            "emergency_contact_phone": new_data_test.emergency_contact_phone_test
        }

        updates_test = {field: value for field, value in field_map_test.items() if value is not None}

        if not updates_test:
            Log.warn("No data has update")
            raise ValueError("No fields to update — all provided fields are None.")
        
        set_clause_test = ", ".join(f"{field} = ?" for field in updates_test.keys())
        values_test = list(updates_test.values())
        values_test.append(id_test)
        query = f"""
        UPDATE students
        SET {set_clause_test}
        WHERE student_id = ?
        """
        self.cursor_test.execute(query, values_test)
        self.conn_test.commit()
        Log.info("Updated Student ID: ", id_test," with data: ", updates_test)
        return self.cursor_test.rowcount > 0

    def deleteStudent_test(self, student_test: Student_test) -> bool:
        if student_test is None:
            Log.warn("deleteStudent failed: student is None")
            return False
        
        query = "DELETE FROM students WHERE student_id = ?"
        self.cursor_test.execute(query, (student_test.id_test,))
        self.conn_test.commit()

        if self.cursor_test.rowcount > 0:
            Log.success(f"Student deleted successfully: ID={student_test.id_test}")
            return True
        else:
            Log.warn(f"No student found with ID={student_test.id_test} failed to delete")
            return False


    def toStudent_test(self, row) -> Student_test:
        return Student_test(
            id_test=row["student_id"],
            first_name_test=row["first_name"],
            last_name_test=row["last_name"],
            email_test=row["email"],
            personal_tutor_email_test=row["personal_tutor_email"],
            emergency_contact_name_test=row["emergency_contact_name"],
            emergency_contact_phone_test=row["emergency_contact_phone"]
        )
    
    def toStudents_test(self,rows) -> List[Student_test]:
        return [self.toStudent_test(row) for row in rows]
