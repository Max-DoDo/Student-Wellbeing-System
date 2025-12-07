from base.entity.student import Student
from base.entity.assessments import Assessment
from base.entity.wellbeing_survey import Wellbeing_Survey
from typing import List, Optional
from base.repository.student_repo import Student_Repo
from base.repository.attendance_repo import Attendance_Repo
from base.repository.assessment_repo import Assessment_Repo
from base.repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
from base.entity.attendance import Attendance

class Student_Service:

    def __init__(self, student_repo: Student_Repo = None, attendance_repo: Attendance_Repo = None, assessment_repo: Assessment_Repo = None, wellbeing_survey_repo: Wellbeing_Survey_Repo = None):
        self.student_repo = student_repo if student_repo else Student_Repo()
        self.attendance_repo = attendance_repo if attendance_repo else Attendance_Repo()
        self.assessment_repo = assessment_repo if assessment_repo else Assessment_Repo()
        self.wellbeing_survey_repo = wellbeing_survey_repo if wellbeing_survey_repo else Wellbeing_Survey_Repo()

    def getAllStudent(self) -> List[Student]:
        return self.student_repo.getAllStudent()
    
    def getAttdenceByID(self, id: int) -> List[Optional[Attendance]]:
        return self.attendance_repo.getAttendancesByStudentID(id);

    def getAssessmentByID(self, id: int) -> List[Optional[Assessment]]:
        return self.assessment_repo.getAssessmentsByStudentID(id);

    def getWellBeingSurveyByID(self, id : int) -> List[Optional[Wellbeing_Survey]]:
        return self.wellbeing_survey_repo.getWellBeingSurveysByStudentID(id);

    def update(self, student = Student):
        Student_Repo().updateStudent(student)

    def add(self, student = Student):
        Student_Repo().addStudent(student)

    def delete(self, student = Student):
        Student_Repo().deleteStudent(student)
