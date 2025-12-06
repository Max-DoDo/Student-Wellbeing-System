from repository.user_repo import User_Repo
from repository.student_repo import Student_Repo
from repository.wellbeing_surveys_repo  import Wellbeing_Survey_Repo
from repository.attendance_repo import Attendance_Repo
from repository.assessment_repo import  Assessment_Repo
from typing import List
from entity.attendance import Attendance
from tools.log import Log

import ssl
import smtplib
import os
import time
from email.message import EmailMessage


class Email_Service:

    wellbeingStuffEmails = []
    profUserEmails = []
    adminUserEmails = []

    students = []
    highStressStudents = []


    def __init__(self, weekNumber):

        self.weekNumber = weekNumber
        self.wellbeingmsg = EmailMessage()
        self.profmsg = EmailMessage()
        self.email = "greatflage@gmail.com"
        self.app_password = "nhynezqutiyblnwh"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.students = Student_Repo().getAllStudent();
        self._getAllUserEmail();
        Log.info("Email service: Start to send weekly report")
    
    def _getAllUserEmail(self):
        users = User_Repo().getAllUser();


        for user in users:
            # 1. if user is not subscribed, skip
            # 2. if user already received a email this week, skip
            # 3. but if user is a test person, ignore the second condition
            # Holy shift
            should_send = (
                user.is_subscribed
                and (
                    user.role_id == -10
                    or user.received_report_at != self.weekNumber
                )
            )

            # Log.debug(f"Sould send: sub: {user.is_subscribed} rcvd: {user.received_report_at == self.weekNumber} ist: {user.role_id == -10} sdsd:{should_send}")
            if should_send:
                if user.role_id == 0:
                    self.adminUserEmails.append(user.email)
                    # Log.info(f"Add {user.email}"f" to \tadmin")
                elif user.role_id == 1:
                    self.wellbeingStuffEmails.append(user.email)
                    # Log.info(f"Add {user.email}"f" to \twellbeing staff")
                elif user.role_id == 2:
                    self.profUserEmails.append(user.email)
                    # Log.info(f"Add {user.email}"f" to \tcourse leader")
                elif user.role_id == -10:
                    self.profUserEmails.append(user.email)
                    self.wellbeingStuffEmails.append(user.email)
                    self.adminUserEmails.append(user.email)
                    # Log.info(f"Add {user.email}"f" to \tTester")
                else:
                    Log.warn(f"Undefined user role with role_id:{user.role_id}are registered in sending Email. {user.email}")
            else:
                Log.info(f"Unable to send Report to {user.name} because this user is NOT THE CHOSEN ONE")


        
    def _getHighStressStudent(self):
        highstressLevel = 4
        lines = []
        for student in self.students:
            wellbeingRecord = Wellbeing_Survey_Repo().getWellBeingSurveysByStudentID(student.id)
            for record in wellbeingRecord:
                if record.stress_level >= highstressLevel and record.week_number == self.weekNumber:
                    lines.append(f"{str(student.id):10}{student.name:30}{record.stress_level:10}{record.week_number:5}")
        body = "\n".join(lines)
        self.wellbeingmsg.set_content(body)

    
    def _getAtRiskStudents(self):

        lowAttendanceLevel = 0.5
        lowAssessmentLevel = 50
        lines = []
        for student in self.students:
            attendanceRecord = Attendance_Repo().getAttendancesByStudentID(student.id)
            if attendanceRecord is not None:
                avg = self._get_attendance_average(attendanceRecord)
                if avg < lowAttendanceLevel:
                    lines.append(f"{str(student.id):10}{student.name:30}{str(avg):10}")
        
        lines.append("")
        lines.append("Low assessment grade student:")
        lines.append("ID        Name                              Average Value")
        lines.append("-------------------------------------------------------------")
        for student in self.students:
            assessmentRecord = Assessment_Repo().getAssessmentsByStudentID(student.id)
            avg = self._get_assessment_average(assessmentRecord)
            if avg is not None and avg < lowAssessmentLevel:
                lines.append(f"{str(student.id):10}{student.name:30}{str(avg):10}")
        body = "\n".join(lines)
        self.profmsg.set_content(body)



    def _get_assessment_average(self,assessment):
        grade = [g.grade for g in assessment]
        if grade is None:
            return None
        return round(sum(grade) / len(grade),2)


    def _get_attendance_average(self,attendance):
        week_records = [r for r in attendance if r.week_number == self.weekNumber]
        if not week_records:
            return None
        bool_values = [r.is_present for r in week_records]
        numeric_values = [1 if v else 0 for v in bool_values]
        return round(sum(numeric_values) / len(numeric_values),2)
    
    def sendEmail(self):
        self._getHighStressStudent()
        self._getAtRiskStudents()
        self._sendToWellBeingStuff()
        self._sendToProfessor()
    
    def _sendToWellBeingStuff(self):

        for email in self.wellbeingStuffEmails:
            user = User_Repo().getUserByEmail(email)
            # Log.debug(user)
# DO NOT TOUCH ANY CODE UNDER THIS LINE WITHOUT PERMISSION||未经允许不要碰这个线以下的所有代码||ห้ามสัมผัสโค้ดใดๆ ที่ต่ำกว่าบรรทัดนี้โดยไม่ได้รับอนุญาต||बिना इजाज़त के इस लाइन के नीचे किसी भी कोड को न छुएं।||Не трогайте код ниже этой строки без разрешения. 
            html_body = f"""
<html>
<body>
Dear {user.username}, I hope this email find you will. Even if this email is automatically generated. Even if I only wrote those once and send to countless people every week.
<h2 style="color:#4A4A4A;">Weekly Wellbeing Report</h2>

<p><b>High Stress Students:</b></p>
<pre>

ID        Name                                   Stress  Week
-------------------------------------------------------------
{self.wellbeingmsg.get_content()}

</pre>
Thank you for your hard work this week!<br>

<p><i>This is an automatically sent email, please do not reply.</i></p>
Best wishes,<br>
Group 4
</body>
</html>
"""
# DO NOT TOUCH ANY CODE ABOVE THIS LINE WITHOUT PERMISSION||未经允许不要碰这个线以上的所有代码||อย่าสัมผัสโค้ดใดๆ เหนือบรรทัดนี้โดยไม่ได้รับอนุญาต||बिना इजाज़त के इस लाइन के ऊपर किसी भी कोड को न छुएं।||Не трогайте код выше этой строки без разрешения.
            try:
                msg = EmailMessage()
                msg["Subject"] = "Weekly Wellbeing Staff Report"
                msg["From"] = "greatflage@gmail.com"
                msg["To"] = email
                msg.set_content("Your email client does not support HTML.")
                msg.add_alternative(html_body, subtype="html")
                context = ssl.create_default_context()

                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.email, self.app_password)
                    server.send_message(msg)
                
                Log.info(f"E-mail sended to: {email} with wellbeing staff report")
            except Exception as e:
                Log.warn("Unable to send E-mail: ", e)
            User_Repo().updateEmailDate(user,self.weekNumber)


    def _sendToProfessor(self):
        for email in self.profUserEmails:
            user = User_Repo().getUserByEmail(email)
# DO NOT TOUCH ANY CODE UNDER THIS LINE WITHOUT PERMISSION||未经允许不要碰这个线以下的所有代码||ห้ามสัมผัสโค้ดใดๆ ที่ต่ำกว่าบรรทัดนี้โดยไม่ได้รับอนุญาต||बिना इजाज़त के इस लाइन के नीचे किसी भी कोड को न छुएं।||Не трогайте код ниже этой строки без разрешения. 
            html_body = f"""
<html>
<body>
Dear {user.username}, I hope this email find you will. Even if this email is automatically generated. Even if I only wrote those once and send to countless people every week.
<h2 style="color:#4A4A4A;">Weekly Course Leader Report</h2>
<pre>
Low attendance student:
ID        Name                              Average Value
-------------------------------------------------------------
{self.profmsg.get_content()}

</pre>
Thank you for your hard work this week!<br>

<p><i>This is an automatically sent email, please do not reply.</i></p>
Best wishes,<br>
Group 4
</body>
</html>
"""
# DO NOT TOUCH ANY CODE ABOVE THIS LINE WITHOUT PERMISSION||未经允许不要碰这个线以上的所有代码||อย่าสัมผัสโค้ดใดๆ เหนือบรรทัดนี้โดยไม่ได้รับอนุญาต||बिना इजाज़त के इस लाइन के ऊपर किसी भी कोड को न छुएं।||Не трогайте код выше этой строки без разрешения.
            try:
                msg = EmailMessage()
                msg["Subject"] = "Weekly Course Leader Report"
                msg["From"] = "greatflage@gmail.com"
                msg["To"] = email
                msg.set_content("Your email client does not support HTML.")
                msg.add_alternative(html_body, subtype="html")
                context = ssl.create_default_context()

                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.email, self.app_password)
                    server.send_message(msg)
                
                Log.info(f"E-mail sended to: {email} with course leader report")
            except Exception as e:
                Log.warn("Unable to send E-mail", e)
            User_Repo().updateEmailDate(user,self.weekNumber)
    def testFunction(self):
        pass



        

