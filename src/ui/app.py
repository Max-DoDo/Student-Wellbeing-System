from flask import Flask, render_template, request, redirect, url_for, session
import plotly.graph_objs as go
import plotly.express as px
import random

app = Flask(__name__)
app.secret_key = "secret123"

# ---- Dummy Users ----
dummy_users = {
    "admin": {"password": "admin", "role": "admin"},
    "wellbeing": {"password": "well", "role": "wellbeing"},
    "leader": {"password": "leader", "role": "course_leader"}
}

# ---- Dummy Student Data ----
students_data = [
   {
       "id": 101, "fname": "John", "lname": "Doe", "course": "CS", "year": 2,
       "email": "john.doe@example.com",
       "personal_tutor_email": "tutor.john@example.com",
       "emergency_contact_name": "Michael Doe",
       "emergency_contact_phone": "999-111-222"
   },
   {
       "id": 102, "fname": "Jane", "lname": "Smith", "course": "Business", "year": 1,
       "email": "jane.smith@example.com",
       "personal_tutor_email": "tutor.jane@example.com",
       "emergency_contact_name": "Sarah Smith",
       "emergency_contact_phone": "888-444-333"
   },
   {
       "id": 103, "fname": "Sam", "lname": "Wilson", "course": "Engineering", "year": 3,
       "email": "sam.wilson@example.com",
       "personal_tutor_email": "tutor.sam@example.com",
       "emergency_contact_name": "Peter Wilson",
       "emergency_contact_phone": "777-555-999"
   },
]

# ---- Dummy Wellbeing Data ----
dummy_wellbeing = {
    101: {"stress": 7, "sleep": 6},
    102: {"stress": 4, "sleep": 7},
    103: {"stress": 9, "sleep": 5}
}

# ---- Dummy Academic Data ----
dummy_academics = {
    101: {"attendance": [88, 90, 85, 92, 87, 91, 89], "grades": [78, 82, 85, 79]},
    102: {"attendance": [70, 72, 68, 75, 73, 71, 74], "grades": [65, 60, 58, 62]},
    103: {"attendance": [95, 96, 94, 97, 93, 95, 96], "grades": [88, 90, 92, 89]}
}

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        # Dummy login logic for now

        # (You will replace this with real DB lookup later)

        if username == "admin" and password == "admin":

            session["role"] = "admin"

            return redirect(url_for("dashboard_redirect"))

        elif username == "well" and password == "well":

            session["role"] = "wellbeing"

            return redirect(url_for("dashboard_redirect"))

        elif username == "leader" and password == "leader":

            session["role"] = "course_leader"

            return redirect(url_for("dashboard_redirect"))

        else:

            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")
 


@app.route("/dashboard")
def dashboard_redirect():
    role = session.get("role")

    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif role == "wellbeing":
        return redirect(url_for("student_list"))
    elif role == "course_leader":
        return redirect(url_for("course_leader_dashboard"))
    else:
        return redirect(url_for("login"))

# ---------------- DASHBOARDS ----------------

@app.route("/admin")
def admin_dashboard():
    return redirect(url_for("student_list"))


@app.route("/wellbeing")
def wellbeing_dashboard():
    return redirect(url_for("student_list"))


@app.route("/course-leader")
def course_leader_dashboard():
    return redirect(url_for("student_list"))

# ---------------- STUDENT LIST ----------------

@app.route("/students")
def student_list():
    return render_template(
        "student_list.html",
        students=students_data,
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
    stress_week = [random.randint(4, 9) for _ in range(7)]
    sleep_week = [random.randint(4, 8) for _ in range(7)]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Plotly Stress Graph
    stress_fig = go.Figure()
    stress_fig.add_trace(go.Scatter(x=days, y=stress_week, mode="lines+markers"))
    stress_fig.update_layout(title="Weekly Stress Trend", height=300)
    stress_chart = stress_fig.to_html(full_html=False)

    # Plotly Sleep Graph
    sleep_fig = go.Figure()
    sleep_fig.add_trace(go.Scatter(x=days, y=sleep_week, mode="lines+markers", line=dict(color="green")))
    sleep_fig.update_layout(title="Weekly Sleep Trend", height=300)
    sleep_chart = sleep_fig.to_html(full_html=False)

    student = next(s for s in students_data if s["id"] == sid)

    return render_template(
        "wellbeing_student_detail.html",
        role=session.get("role"),
        student=student,
        stress_chart=stress_chart,
        sleep_chart=sleep_chart
    )
# ---------------- COURSE LEADER INDIVIDUAL ----------------
@app.route("/course-leader/student/<int:sid>")
def course_leader_student_detail(sid):

    data = dummy_academics[sid]
    attendance_week = data["attendance"]
    grade_list = data["grades"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Attendance chart
    attendance_fig = go.Figure()
    attendance_fig.add_trace(go.Scatter(x=days, y=attendance_week, mode="lines+markers"))
    attendance_fig.update_layout(title="Weekly Attendance Trend", height=300)
    attendance_plot = attendance_fig.to_html(full_html=False)

    # Grades chart
    assignments = [f"A{i+1}" for i in range(len(grade_list))]
    grade_fig = go.Figure()
    grade_fig.add_trace(go.Bar(x=assignments, y=grade_list))
    grade_fig.update_layout(title="Assignment Grades", height=300)
    grade_plot = grade_fig.to_html(full_html=False)

    student = next(s for s in students_data if s["id"] == sid)

    return render_template(
        "course_leader_individual_report.html",
        role=session.get("role"),
        student=student,
        attendance_chart=attendance_plot,
        grade_chart=grade_plot
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
   sid = request.args.get("sid")
   selected = None
   if sid:
       sid = int(sid)
       selected = next(s for s in students_data if s["id"] == sid)
   if request.method == "POST":
       sid = int(request.form["student_id"])
       for s in students_data:
           if s["id"] == sid:
               s["fname"] = request.form["first_name"]
               s["lname"] = request.form["last_name"]
               s["email"] = request.form["email"]
               s["personal_tutor_email"] = request.form["personal_tutor_email"]
               s["emergency_contact_name"] = request.form["emergency_contact_name"]
               s["emergency_contact_phone"] = request.form["emergency_contact_phone"]
       return redirect(url_for("update_student_page", sid=sid))
   return render_template(
       "update_student.html",
       students=students_data,
       selected=selected,
       role=session.get("role")
   )

# ---------------- DELETE STUDENT ----------------

@app.route("/delete-student", methods=["GET", "POST"])
def delete_student_page():
    if session.get("role") != "admin":
        return redirect(url_for("dashboard_redirect"))

    global students_data

    if request.method == "POST":
        sid = int(request.form["student_id"])
        students_data = [s for s in students_data if s["id"] != sid]
        return redirect(url_for("delete_student_page"))

    return render_template(
        "delete_student.html",
        students=students_data,
        role=session.get("role")
    )

# ---------------- ADD STUDENT ----------------
@app.route("/add-student", methods=["GET", "POST"])
def add_student_page():
   if session.get("role") != "admin":
       return redirect(url_for("dashboard_redirect"))
   if request.method == "POST":
       sid = int(request.form["student_id"])
       fname = request.form["first_name"]
       lname = request.form["last_name"]
       email = request.form["email"]
       tutor = request.form["personal_tutor_email"]
       emergency_name = request.form["emergency_contact_name"]
       emergency_phone = request.form["emergency_contact_phone"]
       students_data.append({
           "id": sid,
           "fname": fname,
           "lname": lname,
           "email": email,
           "personal_tutor_email": tutor,
           "emergency_contact_name": emergency_name,
           "emergency_contact_phone": emergency_phone
       })
       return redirect(url_for("student_list"))
   return render_template(
       "add_student.html",
       role=session.get("role")
   )
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
