import unittest
from base.repository.student_repo import Student_Repo
from base.entity.student import Student
from test_refactored.base_repository_test import BaseRepositoryTest

class TestStudentRepo(BaseRepositoryTest):

    def setUp(self):
        self.repo = Student_Repo()

    def test_getStudent(self):
        s = self.repo.getStudent(1)
        self.assertIsNotNone(s)
        # self.assertEqual(s.id, 1)

    def test_getStudent_not_found(self):
        s = self.repo.getStudent(9999)
        self.assertIsNone(s)

    def test_getAllStudent(self):
        students = self.repo.getAllStudent()
        self.assertIsInstance(students, list)
        self.assertGreater(len(students), 0)

if __name__ == "__main__":
    unittest.main()
