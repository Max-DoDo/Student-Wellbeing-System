from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# ---- Dummy Users Based on Roles ----
dummy_users = {
    "admin": {"password": "admin", "role": "admin"},
    "wellbeing": {"password": "well", "role": "wellbeing"},
    "leader": {"password": "leader", "role": "course_leader"}
}

# ---- Dummy Student Data ----
students_data = [
    {"id": 101, "fname": "John", "lname": "Doe", "course": "CS", "year": 2},
    {"id": 102, "fname": "Jane", "lname": "Smith", "course": "Business", "year": 1},
    {"id": 103, "fname": "Sam", "lname": "Wilson", "course": "Engineering", "year": 3}
]


# ---------------- LOGIN PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]

        session["role"] = role
        return redirect(url_for("dashboard_redirect"))

    return render_template("login.html")



@app.route("/dashboard")
def dashboard_redirect():
    role = session.get("role")

    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif role == "wellbeing":
        return redirect(url_for("wellbeing_dashboard"))
    elif role == "course_leader":
        return redirect(url_for("course_leader_dashboard"))
    else:
        return redirect(url_for("login"))



# ---------------- DASHBOARDS ----------------

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html", role=session.get("role"))


@app.route("/wellbeing")
def wellbeing_dashboard():
    return render_template("wellbeing_dashboard.html", role=session.get("role"))


@app.route("/course-leader")
def course_leader_dashboard():
    return render_template("course_leader_dashboard.html", role=session.get("role"))


# ---------------- COMMON PAGES ----------------

@app.route("/students")
def student_list():
    return render_template("student_list.html", students=students_data, role=session.get("role"))


@app.route("/group-report")
def group_report():
    return render_template("group_report.html", role=session.get("role"))


# ---------------- UPDATE / DELETE / ADD ----------------

@app.route("/update-student")
def update_student_page():
    return render_template("update_student.html", students=students_data, role=session.get("role"))


@app.route("/delete-student")
def delete_student_page():
    return render_template("delete_student.html", students=students_data, role=session.get("role"))


@app.route("/add-student")
def add_student_page():
    return render_template("add_student.html", role=session.get("role"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)
