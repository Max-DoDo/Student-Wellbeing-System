from flask import Flask, render_template, request, redirect, url_for, session
import plotly.graph_objs as go
import plotly.express as px
from services.login_service import Login_Service
import random
from repository.user_repo import User_Repo
from repository.student_repo import Student_Repo
from  entity.student import Student
from services.student_service import Student_Service
from repository.wellbeing_surveys_repo import Wellbeing_Survey_Repo
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secret123"
# ---------------- LOGIN ----------------
def get_user_repo():
    return User_Repo()
@app.route("/", methods=["GET", "POST"])
def login():
   if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password")
       # Fetch user from DB
       repo = User_Repo()
       user = repo.getUserByUserName(username)
       if user is None:
           return render_template("login.html", error="User not found")
       # Check if inactive
       if not user.is_active:
           return render_template("login.html", error="Account disabled")
       # Validate password
       if user.password != password:
           return render_template("login.html", error="Incorrect password")
       # -------------------------
    
       session["user_id"] = user.id
       session["username"] = user.username
       # Convert numeric role_id → string role (needed for sidebar)
       if user.role_id == 0:
           session["role"] = "admin"
       elif user.role_id == 1:
           session["role"] = "wellbeing"
       elif user.role_id == 2:
           session["role"] = "course_leader"
       # Redirect based on role_id

       if user.role_id == 0:
           return redirect(url_for("student_list"))
       elif user.role_id == 1:
           return redirect(url_for("student_list"))
       elif user.role_id == 2:
           return redirect(url_for("course_leader_dashboard"))
       return redirect(url_for("dashboard_redirect"))
   return render_template("login.html")


@app.route("/dashboard")
def dashboard_redirect():
    role_id = session.get("role_id")

    if role_id == 0:
        return redirect(url_for("student_list"))
    elif role_id == 1:
        return redirect(url_for("student_list"))
    elif role_id == 2:
        return redirect(url_for("course_leader_dashboard"))
    else:
        return redirect(url_for("login"))

# ---------------- DASHBOARDS ----------------

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html", role=session.get("role"))


@app.route("/wellbeing")
def wellbeing_dashboard():
    return redirect(url_for("student_list"))


@app.route("/course-leader")
def course_leader_dashboard():
    return redirect(url_for("student_list"))

# ---------------- STUDENT LIST ----------------

@app.route("/students")
def student_list():
   repo = Student_Repo()
   students = repo.getAllStudent()  
   return render_template(
       "student_list.html",
       students=students,
       role=session.get("role")
   )


# ---------------- WELLBEING GROUP REPORT ----------------

@app.route("/group-report")
def group_report():
    names = [s["fname"] for s in students_data]
    stress = [dummy_wellbeing[s["id"]]["stress"] for s in students_data]
    sleep = [dummy_wellbeing[s["id"]]["sleep"] for s in students_data]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg Stress", x=names, y=stress))
    fig.add_trace(go.Bar(name="Avg Sleep", x=names, y=sleep))

    fig.update_layout(
        barmode="group",
        title="Group Wellbeing Overview",
        height=400
    )

    chart_html = fig.to_html(full_html=False)

    return render_template(
        "group_report.html",
        role=session.get("role"),
        chart_html=chart_html
    )

# ---------------- WELLBEING INDIVIDUAL ----------------
@app.route("/wellbeing/student/<int:sid>")
def wellbeing_student_detail(sid):
   repo = Wellbeing_Survey_Repo()
   student = Student_Repo().getStudent(sid)
   surveys = repo.getWellBeingSurveysByStudentID(sid)
   if not surveys:
       return render_template(
           "wellbeing_student_detail.html",
           student = student,
           surveys=[],
           charts=[],
           total_weeks=0,
           selected_week=None
       )
   # Convert objects into dicts for HTML
   rows = []
   for s in surveys:
       rows.append({
           "survey_id": s.survey_id,
           "student_id": s.student_id,
           "week_number": s.week_number,
           "stress_level": s.stress_level,
           "hours_slept": s.hours_slept,
           "survey_date": s.survey_date
       })
   # ---- CREATE CHART IMAGES ----
   chart_paths = []
   static_folder = os.path.join(os.path.dirname(__file__), "static")
   os.makedirs(static_folder, exist_ok=True)
   weeks = [r["week_number"] for r in rows]
   stress = [r["stress_level"] for r in rows]
   sleep = [r["hours_slept"] for r in rows]
   # 1. Stress Trend
   plt.figure()
   plt.plot(weeks, stress, marker="o")
   plt.title("Stress Level Over Time")
   plt.xlabel("Week Number")
   plt.ylabel("Stress Level")
   stress_path = os.path.join(static_folder, f"stress_{sid}.png")
   plt.savefig(stress_path)
   chart_paths.append("/static/" + os.path.basename(stress_path))
   plt.close()
   # 2. Sleep Trend
   plt.figure()
   plt.plot(weeks, sleep, marker="o")
   plt.title("Hours Slept Over Time")
   plt.xlabel("Week Number")
   plt.ylabel("Hours Slept")
   sleep_path = os.path.join(static_folder, f"sleep_{sid}.png")
   plt.savefig(sleep_path)
   chart_paths.append("/static/" + os.path.basename(sleep_path))
   plt.close()
   # 3. Stress vs Sleep
   plt.figure()
   plt.scatter(stress, sleep)
   plt.title("Stress vs Sleep")
   plt.xlabel("Stress Level")
   plt.ylabel("Hours Slept")
   comp_path = os.path.join(static_folder, f"comparison_{sid}.png")
   plt.savefig(comp_path)
   chart_paths.append("/static/" + os.path.basename(comp_path))
   plt.close()
   # Total weeks = max week value
   total_weeks = max(weeks)
   return render_template(
       "wellbeing_student_detail.html",
       surveys=rows,
       charts=chart_paths,
       student=student,
       total_weeks=total_weeks,
       selected_week=None
   )
# ---------------- COURSE LEADER INDIVIDUAL ----------------
@app.route("/course-leader/student/<int:sid>")
def course_leader_student_detail(sid):
    # ---- Handle week selection ----
    selected_week = int(request.args.get("week", 1))
    total_weeks = 10
    data = dummy_academics[sid]
    # Attendance for selected week (fake demo: pick one value)
    attendance_week = data["attendance"][selected_week - 1 : selected_week] \
                        + data["attendance"]  # fallback to old behaviour
    # Assignments stay same for all weeks
    grade_list = data["grades"]
    assignments = [f"A{i+1}" for i in range(len(grade_list))]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Attendance Chart (Plotly)
    attendance_fig = go.Figure()
    attendance_fig.add_trace(go.Scatter(x=days, y=data["attendance"], mode="lines+markers"))
    attendance_fig.update_layout(title=f"Attendance Trend – Week {selected_week}", height=300)
    attendance_chart = attendance_fig.to_html(full_html=False)
    # Grades Chart (Plotly)
    grade_fig = go.Figure()
    grade_fig.add_trace(go.Bar(x=assignments, y=grade_list))
    grade_fig.update_layout(title="Assignment Grades", height=300)
    grade_chart = grade_fig.to_html(full_html=False)
    student = next(s for s in students_data if s["id"] == sid)
    return render_template(
        "course_leader_individual_report.html",
        role=session.get("role"),
        student=student,
        attendance_chart=attendance_chart,
        grade_chart=grade_chart,
        selected_week=selected_week,
        total_weeks=total_weeks
    )

# ---------------- COURSE LEADER GROUP REPORT ----------------
@app.route("/course-leader/group-report")
def course_leader_group_report():

    import plotly.graph_objs as go

    names = [s["fname"] for s in students_data]
    avg_attendance = [
        sum(dummy_academics[s["id"]]["attendance"]) / 7 for s in students_data
    ]
    avg_grades = [
        sum(dummy_academics[s["id"]]["grades"]) / len(dummy_academics[s["id"]]["grades"])
        for s in students_data
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Avg Attendance %", x=names, y=avg_attendance))
    fig.add_trace(go.Bar(name="Avg Grade %", x=names, y=avg_grades))

    fig.update_layout(
        barmode="group",
        title="Course Group Academic Overview",
        height=400
    )

    chart_html = fig.to_html(full_html=False)

    return render_template(
        "leader_dashboard.html",
        role=session.get("role"),
        chart_html=chart_html
    )

# ---------------- UPDATE STUDENT ----------------

@app.route("/update-student", methods=["GET", "POST"])
def update_student_page():
   repo = Student_Repo()
   success = False
   # ---------------- POST: UPDATE THE STUDENT ----------------
   if request.method == "POST":
       sid = int(request.form["student_id"])
       # Build a Student object (NOT dict)
       updated_student = Student(
           id=sid,
           first_name=request.form["first_name"],
           last_name=request.form["last_name"],
           email=request.form["email"],
           personal_tutor_email=request.form["personal_tutor_email"],
           emergency_contact_name=request.form["emergency_contact_name"],
           emergency_contact_phone=request.form["emergency_contact_phone"]
       )
       # Call repo correctly
       repo.updateStudent(sid, updated_student)
       # Tell UI success message
       success = True
   # ---------------- GET: LOAD STUDENT LIST ----------------
   students = repo.getAllStudent()
   selected_id = request.args.get("sid")
   selected_student = None
   if selected_id:
       selected_student = repo.getStudent(int(selected_id))
   return render_template(
       "update_student.html",
       students=students,
       selected=selected_student,
       role=session.get("role"),
       success=success
   )
# ---------------- DELETE STUDENT ----------------
@app.route("/delete-student", methods=["GET", "POST"])
def delete_student_page():
   # role for sidebar
   role = session.get("role")
   repo = Student_Repo()
   success = None
   if request.method == "POST":
       sid = int(request.form.get("student_id"))

       student = repo.getStudent(sid)
       if student:
           deleted = repo.deleteStudent(student)
           success = deleted
      
       students = repo.getAllStudent()
       return render_template(
           "delete_student.html",
           students=students,
           role=role,
           success=success
       )
   students = repo.getAllStudent()
   return render_template(
       "delete_student.html",
       students=students,
       role=role
   )
# ---------------- ADD STUDENT ----------------

@app.route("/add-student", methods=["GET", "POST"])
def add_student_page():
   if session.get("role") != "admin":
       return redirect(url_for("dashboard_redirect"))
   repo = Student_Repo()
   success = False   # for alert message
   if request.method == "POST":
       # Read form values
       sid = request.form.get("student_id")
       sid = int(sid) if sid else -1   # if blank → -1 (auto ID)
       first = request.form["first_name"]
       last = request.form["last_name"]
       email = request.form["email"]
       tutor = request.form["personal_tutor_email"]
       em_name = request.form["emergency_contact_name"]
       em_phone = request.form["emergency_contact_phone"]
       # Create Student object (IMPORTANT!)
       student = Student(
           id=sid,
           first_name=first,
           last_name=last,
           email=email,
           personal_tutor_email=tutor,
           emergency_contact_name=em_name,
           emergency_contact_phone=em_phone
       )
       # Add to DB
       repo.addStudent(student)
       success = True
   # Load updated list
   students = repo.getAllStudent()
   return render_template(
       "add_student.html",
       students=students,
       role=session.get("role"),
       success=success
   )
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
#---------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)
