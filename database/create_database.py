import sqlite3
import os
import random

DB_NAME = "university_wellbeing.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER_PATH = os.path.join(BASE_DIR)
DB_FILE_PATH = os.path.join(DB_FOLDER_PATH, DB_NAME)

def init_database():
    if not os.path.exists(DB_FOLDER_PATH):
        os.makedirs(DB_FOLDER_PATH)
        print(f"[INFO] Created directory: {DB_FOLDER_PATH}")

    if os.path.exists(DB_FILE_PATH):
        try:
            os.remove(DB_FILE_PATH)
            print(f"[INFO] Deleted old database: {DB_NAME}")
        except PermissionError:
            print(f"[ERROR] Cannot delete {DB_NAME}. It might be in use.")
            return

    # 3. Connect SQLite
    print(f"[INFO] Creating database at: {DB_FILE_PATH}")
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    # 4. SQL Script
    sql_script = """
    PRAGMA foreign_keys = ON;

    -- usually in sql int 1 is TRUE and 0 is FALSE

    -- 1. Table: Students
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        personal_tutor_email TEXT NOT NULL,
        emergency_contact_name TEXT, 
        emergency_contact_phone TEXT
    );

    -- 2. Table: users
    CREATE TABLE IF NOT EXISTS users (
        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,      -- in first stage we can use plain password
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role_id INTEGER NOT NULL, -- 1 wellbeing users, 2 course leader, 0 admin
        is_active INTEGER DEFAULT 1 CHECK(is_active IN (0, 1)), -- 1=Active, 0=Suspended
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_subscribed INTEGER DEFAULT 1 CHECK(is_subscribed IN (0, 1)),
        received_report_at TIMESTAMP
    );

    -- 3. Table: Attendance
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        week_number INTEGER NOT NULL CHECK(week_number > 0 AND week_number <= 52),
        is_present INTEGER NOT NULL CHECK(is_present IN (0, 1)),
        is_late INTEGER NOT NULL CHECK(is_late IN (0, 1)),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    -- 4. Table: Assessments
    CREATE TABLE IF NOT EXISTS assessments (
        assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        assignment_name TEXT NOT NULL,
        grade INTEGER NOT NULL CHECK(grade >= 0 AND grade <= 100),
        submitted_on_time INTEGER NOT NULL CHECK(submitted_on_time IN (0, 1)),
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    -- 5. Table: Wellbeing Surveys
    CREATE TABLE IF NOT EXISTS wellbeing_surveys (
        survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        week_number INTEGER NOT NULL,
        stress_level INTEGER NOT NULL CHECK(stress_level BETWEEN 1 AND 5),
        hours_slept REAL CHECK(hours_slept >= 0 AND hours_slept <= 24),
        survey_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );

    -- 6. Indexes
    CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);
    CREATE INDEX IF NOT EXISTS idx_survey_student_week ON wellbeing_surveys(student_id, week_number);
    """

    try:
        cursor.executescript(sql_script)
        print("[SUCCESS] Database Schema created successfully.")        
        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] creating database: {e}")
    finally:
        conn.close()

# ==========================================
# Generate Mock Data
# ==========================================

# Mock student names
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
    "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Margaret", "Anthony", "Betty", "Donald", "Sandra",
    "Mark", "Ashley", "Paul", "Dorothy", "Steven", "Kimberly", "Andrew", "Emily", "Kenneth", "Donna",
    "George", "Michelle", "Joshua", "Carol", "Kevin", "Amanda", "Brian", "Melissa", "Edward", "Deborah"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"
]
def get_random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)

def get_random_phone():
    return f"07{random.randint(100000000, 999999999)}"

def populate_database():
    print("\n--- STEP 2: Populating Mock Data (6 Scenarios) ---")
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    # create users
    users = [
    ('admin', 'admin123', 'System', 'Admin', 'admin@warwick.uni.ac.uk', 0, 1, 1, None),
    
    ('wellbeing', 'safe123', 'Sarah', 'Care', 'wellbeing@warwick.uni.ac.uk', 1, 1, 1, None),
    
    ('course_leader', 'teach123', 'Prof', 'Smart', 'course_leader@warwick.uni.ac.uk', 2, 1, 1, None)
    ]
    cursor.executemany("""
        INSERT INTO users (username, password, first_name, last_name, email, role_id, is_active, is_subscribed, received_report_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, users)
    print(f"[INFO] Created {len(users)} system users.")

    # All Scenario
    scenarios = [
        "The Star", "The Burnout", "The Struggler", 
        "The Ghost", "The Smart Skipper", "The Partier"
    ]

    student_id_counter = 1
    
    # 10 persons per scenario
    for student_types in scenarios:
        print(f"  > Generating 10 students for scenario: {student_types}")
        
        for _ in range(10): 
            fname, lname = get_random_name()
            email = f"{fname.lower()}.{lname.lower()}{random.randint(10,99)}@warwick.uni.ac.uk"
            emer_fname, emer_lname = get_random_name()
            emer_name = f"{emer_fname} {emer_lname}"
            emer_phone = get_random_phone()
            
            cursor.execute("""
                INSERT INTO students (student_id, first_name, last_name, email, personal_tutor_email, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (student_id_counter, fname, lname, email, "tutor@warwick.uni.ac.uk", emer_name, emer_phone))

            # create data for 10 weeks
            for week in range(1, 11):
                
                # --- LOGIC: Attendance ---
                is_present = 1
                is_late = 0
                
                if student_types == "The Ghost":
                    is_present = 1 if week <= 3 else 0
                elif student_types in ["The Smart Skipper", "The Partier"]:
                    is_present = 1 if random.random() > 0.6 else 0
                    is_late = 1 if is_present and random.random() > 0.5 else 0
                elif student_types == "The Struggler":
                    is_present = 1 if random.random() > 0.1 else 0
                    is_late = 1 if is_present and random.random() > 0.3 else 0
                else: 
                    is_present = 1
                    is_late = 0

                cursor.execute("INSERT INTO attendance (student_id, week_number, is_present, is_late) VALUES (?,?,?,?)",
                               (student_id_counter, week, is_present, is_late))

                # --- LOGIC: Wellbeing Survey ---
                if student_types == "The Ghost" and week > 3:
                    continue 

                stress = 3
                sleep = 7.0

                if student_types == "The Star":
                    stress = random.randint(1, 2)
                    sleep = random.uniform(7, 9)
                elif student_types == "The Burnout":
                    stress = random.randint(4, 5)
                    sleep = random.uniform(3, 4.5)
                elif student_types == "The Struggler":
                    stress = random.randint(4, 5)
                    sleep = random.uniform(5, 7)
                elif student_types == "The Smart Skipper":
                    stress = random.randint(1, 2)
                    sleep = random.uniform(8, 10)
                elif student_types == "The Partier":
                    stress = random.randint(1, 2)
                    sleep = random.uniform(3, 5)

                if student_types == "The Burnout" or random.random() > 0.15:
                    cursor.execute("INSERT INTO wellbeing_surveys (student_id, week_number, stress_level, hours_slept) VALUES (?,?,?,?)",
                                   (student_id_counter, week, stress, round(sleep, 1)))

            # create grades
            assignments = ["Portfolio", "Midterm Exam", "Group Project"]
            for assign in assignments:
                grade = 50
                on_time = 1

                if student_types in ["The Star", "The Burnout", "The Smart Skipper"]:
                    grade = random.randint(75, 98) 
                elif student_types == "The Struggler":
                    grade = random.randint(35, 49) 
                elif student_types == "The Partier":
                    grade = random.randint(20, 40) 
                elif student_types == "The Ghost":
                    grade = 0
                    on_time = 0

                cursor.execute("INSERT INTO assessments (student_id, assignment_name, grade, submitted_on_time) VALUES (?,?,?,?)",
                               (student_id_counter, assign, grade, on_time))
            
            student_id_counter += 1

    conn.commit()
    conn.close()
    print("[SUCCESS] Mock data populated successfully.")

if __name__ == "__main__":
    init_database()
    populate_database()