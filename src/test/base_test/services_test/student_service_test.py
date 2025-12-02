import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

SRC_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..","..",".."))
sys.path.insert(0, SRC_PATH)

from test.base_test.entity_test.student_test import Student_test
from test.base_test.entity_test.assessments_test import Assessment_test
from test.base_test.entity_test.wellbeing_survey_test import Wellbeing_Survey_test
from typing import List, Optional
from test.base_test.repository_test.student_repo_test import Student_Repo_test
from test.base_test.repository_test.attendance_repo_test import Attendance_Repo_test
from test.base_test.repository_test.assessment_repo_test import Assessment_Repo_test
from test.base_test.repository_test.wellbeing_survey_repo_test import Wellbeing_Survey_Repo_test
from test.base_test.entity_test.attendance_test import Attendance_test

class Student_Service_test:

    '''
    Return value: A list of Student object
    to access the attribute in the student object, see the class file for details.
    '''
    def getAllStudent(self) -> List[Student_test]:
        return Student_Repo_test().getAllStudent()
    
    def getAttdenceByID(self, id: int) -> List[Optional[Attendance_test]]:
        return Attendance_Repo_test().getAttendancesByStudentID(id);

    def getAssessmentByID(self, id: int) -> List[Optional[Assessment_test]]:
        return  Assessment_Repo_test().getAssessmentsByStudentID(id);

    def getWellBeingSurveyByID(self, id : int) -> List[Optional[Wellbeing_Survey_test]]:
        return Wellbeing_Survey_Repo_test().getWellBeingSurveysByStudentID(id);

    def update(self, student = Student_test):
        Student_Repo_test.updateStudent(student)

    def add(self, student = Student_test):
        Student_Repo_test.addStudent(student)

    def delete(self, student = Student_test):
        Student_Repo_test.deleteStudent(student)
