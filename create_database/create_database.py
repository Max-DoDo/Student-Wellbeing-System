import sqlite3
import os

# Database name
DB_NAME = "university_wellbeing.db"

def init_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Deleted old database: {DB_NAME}")

    # 2. connect SQLlite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 3. sql script
    sql_script = """
    PRAGMA foreign_keys = ON;

    # usually in sql int 1 is TRUE and 0 is FALSE

    -- 1. Table: Students
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        personal_tutor_email TEXT NOT NULL,
        emergency_contact_name TEXT, 
        emergency_contact_phone TEXT,
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    -- 7. Views (Privacy Layers)
    CREATE VIEW IF NOT EXISTS view_academic_report AS
    SELECT 
        s.student_id, s.first_name || ' ' || s.last_name AS full_name,
        a.week_number, a.is_present,
        asm.assignment_name, asm.grade
    FROM students s
    LEFT JOIN attendance a ON s.student_id = a.student_id
    LEFT JOIN assessments asm ON s.student_id = asm.student_id;

    CREATE VIEW IF NOT EXISTS view_wellbeing_report AS
    SELECT 
        s.student_id, s.first_name || ' ' || s.last_name AS full_name,
        w.week_number, w.stress_level, w.hours_slept
    FROM students s
    JOIN wellbeing_surveys w ON s.student_id = w.student_id;
    """

    try:
        cursor.executescript(sql_script)
        print("Database Schema created successfully.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()