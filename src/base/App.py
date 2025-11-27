import os
from repository.student_repo import Student_Repo

class App:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))    
        db_folder = os.path.abspath(os.path.join(current_dir, "..", "..", "database"))     
        self.db_path = os.path.join(db_folder, "university_wellbeing.db")   

    def main(self):
        repo = Student_Repo(self.db_path)

        studentsById = repo.getStudent(10)
        students = repo.getAllStudent()
        print(studentsById)
        print(students)

if __name__ == "__main__":
    app = App()
    app.main()