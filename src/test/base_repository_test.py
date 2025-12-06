import unittest
import os
import shutil
import tempfile
from base.repository.base_repo import Base_Repo

class BaseRepositoryTest(unittest.TestCase):
    _original_db_path = "database/university_wellbeing.db"
    _temp_dir = None
    _temp_db_path = None

    @classmethod
    def setUpClass(cls):
        # Create a temporary directory for the test database
        cls._temp_dir = tempfile.mkdtemp()
        cls._temp_db_path = os.path.join(cls._temp_dir, os.path.basename(cls._original_db_path))

        # Copy the original database to the temporary location
        shutil.copyfile(cls._original_db_path, cls._temp_db_path)
        
        # Set the DB_PATH for Base_Repo to the temporary database
        Base_Repo.set_db_path(cls._temp_db_path)

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory and its contents
        if cls._temp_dir and os.path.exists(cls._temp_dir):
            shutil.rmtree(cls._temp_dir)
            cls._temp_dir = None
            cls._temp_db_path = None

    def setUp(self):
        pass

    def tearDown(self):
        pass
