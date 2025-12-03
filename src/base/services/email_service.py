from repository.user_repo import User_Repo
from typing import List
from tools.log import Log

import ssl
import smtplib
import os
import time
from email.message import EmailMessage


class Email_Service:

    def __init__(self):

        self.email = "greatflage@gmail.com"
        self.app_password = "nhynezqutiyblnwh"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465

    def sendEmail(self):
        try:
            msg = EmailMessage()
            msg["Subject"] = "test email"
            msg["From"] = "greatflage@gmail.com"
            msg["To"] = "great_maxwell@outlook.com"
            msg.set_content("come from python。")
            context = ssl.create_default_context()


            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.email, self.app_password)
                server.send_message(msg)
            
            Log.info("邮件发送成功！")
        except Exception as e:
            Log.warn("发送失败：", e)

    def testFunction(self):
        pass



        

