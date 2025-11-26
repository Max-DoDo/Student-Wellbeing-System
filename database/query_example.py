import os
import sqlite3

DB_NAME = "university_wellbeing.db"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER_PATH = os.path.join(BASE_DIR)
DB_FILE_PATH = os.path.join(DB_FOLDER_PATH, DB_NAME)

conn = sqlite3.connect(DB_FILE_PATH)
cursor = conn.cursor()

query = "SELECT * FROM users"

cursor.execute(query)

results = cursor.fetchall()

print(f"{'username':<5} {'firstname':<20} {'lastname':<5} {'email':<7} {'roleid'} {'isactive'}")
print("-" * 50)

for row in results:
    username = row[1]
    firstname = row[3]
    lastname = row[4]
    email = row[5]
    roleid = row[6]
    isactive = row[7]

    print(f"{username:<5} {firstname:<20} {lastname:<5} {email:<7} {roleid} {isactive}")

conn.close()