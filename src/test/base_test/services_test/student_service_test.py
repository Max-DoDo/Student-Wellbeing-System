from entity_test.student_test import Student_test
from entity_test.assessments_test import Assessment_test
from entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from typing import List, Optional
from repository_test.student_repo_test import Student_Repo_test
from repository_test.attendance_repo_test import Attendance_Repo_test
from repository_test.assessment_repo_test import Assessment_Repo_test
from repository_test.wellbeing_survey_repo_test import Wellbeing_Survey_Repo_test
from entity_test.attendance_test import Attendance_test

class Student_Service_test:

    '''
    Return value: A list of Student object
    to access the attribute in the student object, see the class file for details.
    '''
    def getAllStudent_test(self) -> List[Student_test]:
        return Student_Repo_test().getAllStudent_test()
    
    def getAttdenceByID_test(self, id_test: int) -> List[Optional[Attendance_test]]:
        return Attendance_Repo_test().getAttendancesByStudentID_test(id_test)

    def getAssessmentByID_test(self, id_test: int) -> List[Optional[Assessment_test]]:
        return Assessment_Repo_test().getAssessmentsByStudentID_test(id_test)

    def getWellBeingSurveyByID_test(self, id_test : int) -> List[Optional[Wellbeing_Survey_test]]:
        return Wellbeing_Survey_Repo_test().getWellBeingSurveysByStudentID_test(id_test)

    def update_test(self, student_test = Student_test):
        Student_Repo_test.updateStudent_test(student_test)

    def add_test(self, student_test = Student_test):
        Student_Repo_test.addStudent_test(student_test)

    def delete_test(self, student_test = Student_test):
        Student_Repo_test.deleteStudent_test(student_test)
