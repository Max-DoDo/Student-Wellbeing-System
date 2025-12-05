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

    '''
    Return value: A list of Student object
    to access the attribute in the student object, see the class file for details.
    '''
    def getAllStudent(self) -> List[Student]:
        return Student_Repo().getAllStudent()
    
    def getAttdenceByID(self, id: int) -> List[Optional[Attendance]]:
        return Attendance_Repo().getAttendancesByStudentID(id);

    def getAssessmentByID(self, id: int) -> List[Optional[Assessment]]:
        return  Assessment_Repo().getAssessmentsByStudentID(id);

    def getWellBeingSurveyByID(self, id : int) -> List[Optional[Wellbeing_Survey]]:
        return Wellbeing_Survey_Repo().getWellBeingSurveysByStudentID(id);

    def update(self, student = Student):
        Student_Repo.updateStudent(student)

    def add(self, student = Student):
        Student_Repo.addStudent(student)

    def delete(self, student = Student):
        Student_Repo.deleteStudent(student)