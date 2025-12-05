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
import plotly.graph_objects as go
import plotly.io as pio
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.graph_objects as go
from repository.attendance_repo import Attendance_Repo
from repository.attendance_repo import Attendance_Repo
from repository.assessment_repo import Assessment_Repo

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
      
       repo = User_Repo()
       user = repo.getUserByUserName(username)
       if user is None:
           return render_template("login.html", error="User not found")
       
       if not user.is_active:
           return render_template("login.html", error="Account disabled")
       
       if user.password != password:
           return render_template("login.html", error="Incorrect password")
       
    
       session["user_id"] = user.id
       session["username"] = user.username
       session["role_id"] = user.role_id
       session["role"] = (
           "admin" if user.role_id == 0 else
           "wellbeing" if user.role_id == 1 else
           "course_leader"
       )
       if user.role_id == 0:
           session["role"] = "admin"
       elif user.role_id == 1:
           session["role"] = "wellbeing"
       elif user.role_id == 2:
           session["role"] = "course_leader"

       if user.role_id == 0:
           return redirect(url_for("admin_dashboard"))
       elif user.role_id == 1:
           return redirect(url_for("wellbeing_dashboard"))
       elif user.role_id == 2:
           return redirect(url_for("course_leader_dashboard"))
       return redirect(url_for("dashboard_redirect"))
   return render_template("login.html", login_error = "Wrong Username or Password")


@app.route("/dashboard")
def dashboard_redirect():
    role_id = session.get("role_id")

    if role_id == 0:
        return redirect(url_for("admin_dashboard"))
    elif role_id == 1:
        return redirect(url_for("wellbeing_dashboard"))
    elif role_id == 2:
        return redirect(url_for("course_leader_dashboard"))
    else:
        return redirect(url_for("login"))

# ---------------- DASHBOARDS ----------------

@app.route("/admin")
def admin_dashboard():
   student_repo = Student_Repo()
   survey_repo = Wellbeing_Survey_Repo()
   attendance_repo = Attendance_Repo()
   assessment_repo = Assessment_Repo()
   total_students = len(student_repo.getAllStudent() or [])
   total_surveys = len(survey_repo.getWellBeingSurveys() or [])
   total_attendance = len(attendance_repo.getAllAttendance() or [])
   total_assessments = len(assessment_repo.getAssessments() or [])
   return render_template(
       "admin_dashboard.html",
       role=session.get("role"),
       total_students=total_students,
       total_surveys=total_surveys,
       total_attendance=total_attendance,
       total_assessments=total_assessments
   )


@app.route("/wellbeing")
def wellbeing_dashboard():
   survey_repo = Wellbeing_Survey_Repo()
   student_repo = Student_Repo()
   students = student_repo.getAllStudent()
   surveys = survey_repo.getWellBeingSurveys()
   total_students = len(students)

   if surveys:
       avg_stress = round(sum(s.stress_level for s in surveys) / len(surveys), 2)
       avg_sleep = round(sum(s.hours_slept for s in surveys) / len(surveys), 2)
   else:
       avg_stress = "N/A"
       avg_sleep = "N/A"
   
   high_risk_students = []
   for student in students:
       s_surveys = survey_repo.getWellBeingSurveysByStudentID(student.id)
       if not s_surveys:
           continue
       avg_s = sum(x.stress_level for x in s_surveys) / len(s_surveys)
       avg_h = sum(x.hours_slept for x in s_surveys) / len(s_surveys)
       
       if avg_s >= 4 or avg_h <= 5:
        high_risk_students.append({
       "id": student.id,
       "name": f"{student.first_name} {student.last_name}",
       "avg_stress": round(avg_s, 2),
       "avg_sleep": round(avg_h, 2)
   })
   return render_template(
       "wellbeing_dashboard.html",
       role=session.get("role"),
       total_students=total_students,
       avg_stress=avg_stress,
       avg_sleep=avg_sleep,
       high_risk_students=high_risk_students
   )

@app.route("/course-leader")
def course_leader_dashboard():
   student_repo = Student_Repo()
   att_repo = Attendance_Repo()
   grade_repo = Assessment_Repo()
   students = student_repo.getAllStudent()

   total_students = len(students)
   
   all_att = att_repo.getAllAttendance()
   if all_att:
       avg_attendance = round(sum(a.is_present for a in all_att) / len(all_att) * 100, 2)
   else:
       avg_attendance = "N/A"
   
   all_grades = grade_repo.getAssessments()
   if all_grades:
       avg_grade = round(sum(g.grade for g in all_grades) / len(all_grades), 2)
   else:
       avg_grade = "N/A"
   
   high_risk_students = []
   for s in students:
       attendance = att_repo.getAttendancesByStudentID(s.id)
       grades = grade_repo.getAssessmentsByStudentID(s.id)
       if not attendance or not grades:
           continue
       attendance_rate = sum(a.is_present for a in attendance) / len(attendance)
       avg_student_grade = sum(g.grade for g in grades) / len(grades)
       if attendance_rate < 0.50 or avg_student_grade < 50:
           high_risk_students.append({
               "id": s.id,
               "name": f"{s.first_name} {s.last_name}",
               "attendance": round(attendance_rate * 100, 1),
               "grade": round(avg_student_grade, 1)
           })
   return render_template(
       "course_leader_dashboard.html",
       role=session.get("role"),
       total_students=total_students,
       avg_attendance=avg_attendance,
       avg_grade=avg_grade,
       high_risk_students=high_risk_students
   )

# ---------------- STUDENT LIST ----------------

@app.route("/students")
def student_list():
   repo = Student_Repo()
   students = repo.getAllStudent()
   sort_key = request.args.get("sort")
   sort = sort_key  
   if sort_key == "first_name":
       students.sort(key=lambda s: (s.first_name or "").lower())
   elif sort_key == "last_name":
       students.sort(key=lambda s: (s.last_name or "").lower())
   elif sort_key == "id":
       students.sort(key=lambda s: s.id)
   return render_template(
       "student_list.html",
       students=students,
       role=session.get("role"),
       sort=sort
   )

# ---------------- WELLBEING GROUP REPORT ----------------

@app.route("/group-report")
def group_report():
   survey_repo = Wellbeing_Survey_Repo()
   student_repo = Student_Repo()
   att_repo = Attendance_Repo()
   students = student_repo.getAllStudent()
   surveys_all = survey_repo.getWellBeingSurveys()
   if not surveys_all:
       return render_template(
           "group_report.html",
           role=session.get("role"),
           avg_stress_chart="No data available.",
           avg_sleep_chart="No data available.",
           stress_distribution_chart="No data available."
       )
   week_map = {}
   sleep_map = {}
   for s in surveys_all:
       week_map.setdefault(s.week_number, []).append(s.stress_level)
       sleep_map.setdefault(s.week_number, []).append(s.hours_slept)
   weeks = sorted(week_map.keys())
   avg_stress = [round(sum(v) / len(v), 2) for v in week_map.values()]
   avg_sleep = [round(sum(v) / len(v), 2) for v in sleep_map.values()]
   stress_fig = go.Figure()
   stress_fig.add_trace(go.Scatter(
       x=weeks,
       y=avg_stress,
       mode="lines+markers",
       marker=dict(size=8)
   ))
   stress_fig.update_layout(
       title="Average Stress Level per Week",
       xaxis_title="Week Number",
       yaxis_title="Stress Level (1–5)",
       template="plotly_white",
       height=350
   )
   avg_stress_chart = stress_fig.to_html(full_html=False)
   sleep_fig = go.Figure()
   sleep_fig.add_trace(go.Scatter(
       x=weeks,
       y=avg_sleep,
       mode="lines+markers",
       marker=dict(size=8)
   ))
   sleep_fig.update_layout(
       title="Average Sleep Hours per Week",
       xaxis_title="Week Number",
       yaxis_title="Hours Slept",
       template="plotly_white",
       height=350
   )
   avg_sleep_chart = sleep_fig.to_html(full_html=False)
   stress_groups = {
       "Low Stress (1–2)": 0,
       "Moderate Stress (2–3.5)": 0,
       "High Stress (3.5+)": 0
   }
   for st in students:
       st_surveys = survey_repo.getWellBeingSurveysByStudentID(st.id)
       if not st_surveys:
           continue
       avg_s = sum(s.stress_level for s in st_surveys) / len(st_surveys)
       if avg_s <= 2:
           stress_groups["Low Stress (1–2)"] += 1
       elif avg_s <= 3.5:
           stress_groups["Moderate Stress (2–3.5)"] += 1
       else:
           stress_groups["High Stress (3.5+)"] += 1
   pie_fig = go.Figure(
       data=[go.Pie(
           labels=list(stress_groups.keys()),
           values=list(stress_groups.values()),
           hole=0.4
       )]
   )
   pie_fig.update_layout(
       title="Student Stress Distribution (All Students)",
       height=350
   )
   stress_distribution_chart = pie_fig.to_html(full_html=False)

   return render_template(
       "group_report.html",
       role=session.get("role"),
       avg_stress_chart=avg_stress_chart,
       avg_sleep_chart=avg_sleep_chart,
       stress_distribution_chart=stress_distribution_chart
   )

# ---------------- WELLBEING INDIVIDUAL ----------------
@app.route("/wellbeing/student/<int:sid>")
def wellbeing_student_detail(sid):
   survey_repo = Wellbeing_Survey_Repo()
   student_repo = Student_Repo()

   student = student_repo.getStudent(sid)
   if not student:
       return "<h3>Student not found.</h3>", 404
  
   surveys = survey_repo.getWellBeingSurveysByStudentID(sid) or []
   if not surveys:
       return render_template(
           "wellbeing_student_detail.html",
           role=session.get("role"),
           student=student,
           avg_stress="N/A",
           avg_sleep="N/A",
           stress_chart="<p>No wellbeing data available.</p>",
           sleep_chart="<p>No wellbeing data available.</p>",
           stress_sleep_charts="<p>No data</p>",
           pie_chart="<p>No submission related chart for wellbeing.</p>",
           warnings=[],
           weekly_rows=[]
       )

   avg_stress = round(sum(s.stress_level for s in surveys) / len(surveys), 2)
   avg_sleep = round(sum(s.hours_slept for s in surveys) / len(surveys), 2)
 
   warnings = []
   if avg_stress >= 4:
       warnings.append("⚠ High average stress level detected.")
   if avg_sleep <= 5:
       warnings.append("⚠ Consistently low sleep duration detected.")

   weeks = [s.week_number for s in surveys]
   stress_vals = [s.stress_level for s in surveys]
   stress_fig = go.Figure()
   stress_fig.add_trace(go.Scatter(
       x=weeks, y=stress_vals, mode="lines+markers", name="Stress Level"
   ))
   stress_fig.update_layout(
       title="Stress Level Across Weeks",
       xaxis_title="Week",
       yaxis_title="Stress (1–5)",
       template="plotly_white",
       height=300
   )
   stress_chart = stress_fig.to_html(full_html=False)
 
   sleep_vals = [s.hours_slept for s in surveys]
   sleep_fig = go.Figure()
   sleep_fig.add_trace(go.Scatter(
       x=weeks, y=sleep_vals, mode="lines+markers", name="Sleep (hrs)"
   ))
   sleep_fig.update_layout(
       title="Sleep Hours Across Weeks",
       xaxis_title="Week",
       yaxis_title="Hours Slept",
       template="plotly_white",
       height=300
   )
   sleep_chart = sleep_fig.to_html(full_html=False)

   high = len([s for s in surveys if s.stress_level >= 4])
   normal = len(surveys) - high
   pie_fig = go.Figure(data=[go.Pie(
       labels=["High Stress", "Normal"],
       values=[high, normal],
       hole=0.45
   )])
   pie_fig.update_layout(title="Stress Severity Breakdown", height=300)
   pie_chart = pie_fig.to_html(full_html=False)
   weekly_rows = []
   for s in sorted(surveys, key=lambda x: x.week_number):
       weekly_rows.append({
           "week": s.week_number,
           "stress": s.stress_level,
           "sleep": s.hours_slept
       })
   return render_template(
       "wellbeing_student_detail.html",
       role=session.get("role"),
       student=student,
       avg_stress=avg_stress,
       avg_sleep=avg_sleep,
       stress_chart=stress_chart,
       sleep_chart=sleep_chart,
       pie_chart=pie_chart,
       warnings=warnings,
       weekly_rows=weekly_rows,
   )

# ---------------- COURSE LEADER INDIVIDUAL ----------------
@app.route("/course-leader/student/<int:sid>")
def course_leader_student_detail(sid):
   student_repo = Student_Repo()
   att_repo = Attendance_Repo()
   grade_repo = Assessment_Repo()
   student = student_repo.getStudent(sid)
   if not student:
       return "<h3>Student not found.</h3>"
   attendance = att_repo.getAttendancesByStudentID(sid) or []
   grades = grade_repo.getAssessmentsByStudentID(sid) or []
   # ---- AVERAGES ----
   avg_attendance = (
       round(sum(a.is_present for a in attendance) / len(attendance) * 100, 2)
       if attendance else 0
   )
   avg_grade = (
       round(sum(g.grade for g in grades) / len(grades), 2)
       if grades else 0
   )
   # ---- ALERTS ----
   alerts = []
   if avg_attendance < 60:
       alerts.append("⚠ Low Attendance Risk")
   if avg_grade < 40:
       alerts.append("⚠ Failing Average Grade")
   # ---- ATTENDANCE TREND (with red line for absence) ----
   weeks = [a.week_number for a in attendance]
   present_vals = [1 if a.is_present else 0 for a in attendance]
   att_fig = go.Figure()
   # Build line segments week → week (with colour per segment)
   for i in range(len(weeks) - 1):
       x_segment = [weeks[i], weeks[i+1]]
       y_segment = [present_vals[i], present_vals[i+1]]
       # Entire segment = red if ANY of the two points is 0
       seg_color = "#ff0000" if (y_segment[0] == 0 or y_segment[1] == 0) else "#1f77b4"
       att_fig.add_trace(go.Scatter(
           x=x_segment,
           y=y_segment,
           mode="lines",
           line=dict(width=3, color=seg_color),
           showlegend=False
       ))
   # Add markers (blue = present, red = absent)
   marker_colors = ["#1f77b4" if v == 1 else "#ff0000" for v in present_vals]
   att_fig.add_trace(go.Scatter(
       x=weeks,
       y=present_vals,
       mode="markers",
       marker=dict(size=10, color=marker_colors),
       showlegend=False
   ))
   att_fig.update_layout(
       title="Attendance Trend (Present = 1, Absent = 0)",
       xaxis_title="Week",
       yaxis_title="Present / Absent",
       yaxis=dict(range=[-0.1, 1.1]),
       template="plotly_white",
       height=330
   )
   attendance_chart = att_fig.to_html(full_html=False)
   # ---- GRADES BAR CHART ----
   if grades:
       labels = [g.assignment_name for g in grades]
       grade_vals = [g.grade for g in grades]
       grade_fig = go.Figure()
       grade_fig.add_trace(go.Bar(x=labels, y=grade_vals))
       grade_fig.update_layout(
           title="Assignment Grade Performance",
           yaxis_title="Grade (%)",
           template="plotly_white",
           height=330
       )
       grade_chart = grade_fig.to_html(full_html=False)
   else:
       grade_chart = "<p>No grade data available.</p>"
   # ---- SUBMISSION PIE CHART ----
   if grades:
       on_time = sum(1 for g in grades if g.submitted_on_time == 1)
       late = sum(1 for g in grades if g.submitted_on_time == 0)
       pie_fig = go.Figure(data=[go.Pie(
           labels=["Submitted On Time", "Late Submission"],
           values=[on_time, late],
           hole=0.45
       )])
       pie_fig.update_layout(
           title="Submission Timeliness",
           height=290
       )
       submission_pie = pie_fig.to_html(full_html=False)
   else:
       submission_pie = "<p>No submission data.</p>"
   # ---- WEEKLY SUMMARY TABLE ----
   weekly_summary = []
   for w in sorted(set(a.week_number for a in attendance)):
       week_att = [a for a in attendance if a.week_number == w]
       att_percent = round(sum(a.is_present for a in week_att) / len(week_att) * 100, 2)
       weekly_summary.append({
           "week": w,
           "attendance": att_percent
       })
   return render_template(
       "course_leader_individual_report.html",
       role=session.get("role"),
       student=student,
       avg_attendance=avg_attendance,
       avg_grade=avg_grade,
       attendance_chart=attendance_chart,
       grade_chart=grade_chart,
       submission_pie=submission_pie,
       alerts=alerts,
       weekly_summary=weekly_summary
   )
# ---------------- COURSE LEADER GROUP REPORT ----------------
@app.route("/course-leader/group-report")
def course_leader_group_report():
   student_repo = Student_Repo()
   att_repo = Attendance_Repo()
   grade_repo = Assessment_Repo()
   students = student_repo.getAllStudent()
   # -------------------------
   # 1. WEEKLY ATTENDANCE AVG
   # -------------------------
   attendance_all = att_repo.getAllAttendance()
   if not attendance_all:
       weeks = []
       avg_attendance = []
   else:
       attendance_map = {}
       for a in attendance_all:
           attendance_map.setdefault(a.week_number, []).append(a.is_present)
       weeks = sorted(attendance_map.keys())
       avg_attendance = [
           round(sum(vals) / len(vals) * 100, 1)
           for vals in attendance_map.values()
       ]
   att_fig = go.Figure()
   att_fig.add_trace(go.Scatter(
       x=weeks,
       y=avg_attendance,
       mode="lines+markers",
       marker=dict(size=8)
   ))
   att_fig.update_layout(
       title="Average Attendance Per Week (%)",
       xaxis_title="Week Number",
       yaxis_title="Avg Attendance %",
       template="plotly_white",
       height=350
   )
   attendance_chart = att_fig.to_html(full_html=False)
   # -------------------------
   # 2. AVERAGE GRADE CHART
   # -------------------------
   grades_all = grade_repo.getAssessments()
   assignment_map = {}
   if grades_all:
       for g in grades_all:
           assignment_map.setdefault(g.assignment_name, []).append(g.grade)
       assignments = list(assignment_map.keys())
       avg_grades = [
           round(sum(assignment_map[a]) / len(assignment_map[a]), 1)
           for a in assignments
       ]
   else:
       assignments = []
       avg_grades = []
   grade_fig = go.Figure()
   grade_fig.add_trace(go.Bar(x=assignments, y=avg_grades))
   grade_fig.update_layout(
       title="Average Grade Per Assignment",
       xaxis_title="Assessment",
       yaxis_title="Average Grade (%)",
       template="plotly_white",
       height=350
   )
   grade_chart = grade_fig.to_html(full_html=False)
   # -------------------------
   # 3. ACADEMIC RISK CHART
   # -------------------------
   def academic_risk(att_rate, avg_grade):
       if att_rate < 50 or avg_grade < 40:
           return "High Risk"
       if att_rate < 75 or avg_grade < 60:
           return "Moderate Risk"
       return "Low Risk"
   category_count = {"No Data": 0, "Low Risk": 0, "Moderate Risk": 0, "High Risk": 0}
   for st in students:
       st_att = att_repo.getAttendancesByStudentID(st.id)
       st_grades = grade_repo.getAssessmentsByStudentID(st.id)
       if not st_att or not st_grades:
           category_count["No Data"] += 1
       else:
           att_rate = sum(a.is_present for a in st_att) / len(st_att) * 100
           avg_grade = sum(g.grade for g in st_grades) / len(st_grades)
           cat = academic_risk(att_rate, avg_grade)
           category_count[cat] += 1
   labels = ["No Data", "Low Risk", "Moderate Risk", "High Risk"]
   values = [category_count[l] for l in labels]
   colors = ["#b39ddb", "#66bb6a", "#42a5f5", "#ef5350"]  # pastel / clean colours
   risk_fig = go.Figure(
       data=[go.Pie(
           labels=labels,
           values=values,
           hole=0.45,
           marker=dict(colors=colors)
       )]
   )
   risk_fig.update_layout(
       title="Academic Risk Distribution For All Students",
       height=350
   )
   category_chart = risk_fig.to_html(full_html=False)
   # -------------------------
   # 4. SUBMISSION PIE CHART
   # -------------------------
   submitted = sum(1 for g in grades_all if g.submitted_on_time == 1) if grades_all else 0
   late = sum(1 for g in grades_all if g.submitted_on_time == 0) if grades_all else 0
   submission_fig = go.Figure(
       data=[go.Pie(
           labels=["Submitted On Time", "Late Submission"],
           values=[submitted, late],
           marker=dict(colors=["#4CAF50", "#FF5252"]),
           hole=0.45
       )]
   )
   submission_fig.update_layout(
       title="Coursework Submission Rate For All Students",
       height=350
   )
   submission_chart = submission_fig.to_html(full_html=False)
   # -------------------------
   # RETURN
   # -------------------------
   return render_template(
       "leader_dashboard.html",
       role=session.get("role"),
       attendance_chart=attendance_chart,
       grade_chart=grade_chart,
       category_chart=category_chart,
       submission_chart=submission_chart
   )
# ---------------- UPDATE STUDENT ----------------

@app.route("/update-student", methods=["GET", "POST"])
def update_student_page():
   repo = Student_Repo()
   success = False
   error_message = None    
   if request.method == "POST":
       sid = int(request.form["student_id"])
 
       new_email = request.form["email"]
     
       all_students = repo.getAllStudent()
       for s in all_students:
           if s.email == new_email and s.id != sid:
               error_message = "Email already exists for another student."
               break
       if error_message:
           
           students = repo.getAllStudent()
           selected_student = repo.getStudent(sid)
           return render_template(
               "update_student.html",
               students=students,
               selected=selected_student,
               role=session.get("role"),
               success=False,
               error=error_message
           )
       updated_student = Student(
           id=sid,
           first_name=request.form["first_name"],
           last_name=request.form["last_name"],
           email=new_email,
           personal_tutor_email=request.form["personal_tutor_email"],
           emergency_contact_name=request.form["emergency_contact_name"],
           emergency_contact_phone=request.form["emergency_contact_phone"]
       )
       repo.updateStudent(updated_student)
       success = True
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
       success=success,
       error=error_message
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
   success = False
   error = None     
   if request.method == "POST":
       
       sid = request.form.get("student_id")
       sid = int(sid) if sid else -1
       first = request.form["first_name"]
       last = request.form["last_name"]
       email = request.form["email"]
       tutor = request.form["personal_tutor_email"]
       em_name = request.form["emergency_contact_name"]
       em_phone = request.form["emergency_contact_phone"]
       
       students = repo.getAllStudent()
       id_exists = any(s.id == sid for s in students) if sid != -1 else False
       email_exists = any(s.email.lower() == email.lower() for s in students)
       if id_exists and email_exists:
           error = "A student with this ID and Email already exists!"
       elif id_exists:
           error = "Student ID already exists!"
       elif email_exists:
           error = "A student with this Email already exists!"
       
       if error:
           return render_template(
               "add_student.html",
               students=students,
               role=session.get("role"),
               success=False,
               error=error
           )
       student = Student(
           id=sid,
           first_name=first,
           last_name=last,
           email=email,
           personal_tutor_email=tutor,
           emergency_contact_name=em_name,
           emergency_contact_phone=em_phone
       )
       repo.addStudent(student)
       success = True
   students = repo.getAllStudent()
   return render_template(
       "add_student.html",
       students=students,
       role=session.get("role"),
       success=success,
       error=error
   )
# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
