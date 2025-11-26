import sqlite3

DB_NAME = "university_wellbeing.db"

def init_users_plaintext():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"Connected to {DB_NAME}")

    # create sample users data
    # Role Mapping: 0=Admin, 1=Wellbeing, 2=Course Leader
    users_data = [
        # --- Role 0: Admin ---
        ('admin_main', 'admin1234', 'System', 'Administrator', 'admin@uni.ac.uk', 0, 1),
        
        # --- Role 2: Course Leaders ---
        ('ajarn_somchai', 'somchai123', 'Somchai', 'Jaidee', 'somchai.j@uni.ac.uk', 2, 1),
        ('ajarn_suda',    'suda123',    'Suda',    'Rakrian', 'suda.r@uni.ac.uk',    2, 1),
        ('prof_snape',    'magic123',   'Severus', 'Snape',   'snape@uni.ac.uk',     2, 1),
        ('dr_manee',      'manee123',   'Manee',   'Meeta',   'manee.m@uni.ac.uk',   2, 1),

        # --- Role 1: Wellbeing Users ---
        ('nurse_joy',     'joy123',     'Joy',     'Pokemon', 'joy@uni.ac.uk',       1, 1),
        ('counselor_t',   'troi123',    'Deanna',  'Troi',    'troi@uni.ac.uk',      1, 1),
        ('psy_somying',   'somying123', 'Somying', 'Jitdee',  'somying.j@uni.ac.uk', 1, 1),
        ('dr_phil',       'phil123',    'Phil',    'McGraw',  'phil@uni.ac.uk',      1, 1),

        # --- Role 2: Suspended User ---
        ('bad_teacher',   'bad123',     'Bad',     'Guy',     'bad.guy@uni.ac.uk',   2, 0)
    ]

    # 4. Insert database
    insert_sql = """
    INSERT INTO users (username, password, first_name, last_name, email, role_id, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.executemany(insert_sql, users_data)
        conn.commit()
        print(f"Successfully inserted {cursor.rowcount} users (Plain Text Passwords).")
        
        print("-" * 50)
        cursor.execute("SELECT username, password, role_id FROM users LIMIT 5")
        for row in cursor.fetchall():
            print(f"User: {row[0]:<15} | Pass: {row[1]:<12} | Role: {row[2]}")
            
    except sqlite3.IntegrityError as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_users_plaintext()