import sqlite3

# 1. เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect("university_wellbeing.db")
cursor = conn.cursor()

# 2. เขียนคำสั่ง SQL (ลองดึงข้อมูลจาก View ที่เราสร้างไว้)
# เลือกดูรายงานความเครียด (Wellbeing Officer View)
query = "SELECT * FROM users"

# 3. สั่งรันคำสั่ง
cursor.execute(query)

# 4. ดึงผลลัพธ์ทั้งหมดออกมา (fetchall)
results = cursor.fetchall()

# 5. แสดงผล (วนลูปดูทีละแถว)
print("--- รายงานสุขภาพจิตนักศึกษา (Wellbeing Report) ---")
print(f"{'ID':<5} {'Name':<20} {'Week':<5} {'Stress':<7} {'Sleep (hr)'}")
print("-" * 50)

for row in results:
    # row จะเป็น Tuple เช่น (1, 'Somchai Dee', 'alice@uni...', ..., 4, 6.5)
    student_id = row[0]
    name = row[1]
    week = row[2]
    stress = row[3]
    sleep = row[4]
    
    print(f"{student_id:<5} {name:<20} {week:<5} {stress:<7} {sleep}")

# 6. ปิดการเชื่อมต่อ
conn.close()