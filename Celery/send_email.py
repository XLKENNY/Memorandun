# linux
# Celery
# send_email.py 
# author:KENNY


import smtplib
import os
import sys
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_password():
    """return  password"""
    password = 'vqdirswphxcfhggd'
    return password


class MailMaster:
    """Operations on mailboxes"""
    def __init__(self, id, password, name,email_address, smtp_server='smtp.qq.com', email_addr='xulei2412@foxmail.com'):
        self.smtp = SMTP_SSL(smtp_server)
        self.smtp.ehlo(smtp_server)
        self.smtp.login(email_addr, password)
        self.email_sender = email_addr
        self.email_recipients = email_address
        self.name = name

    def notice(self, username, text, subject='memorandum'):
        """An email that sends notification information"""
        self.send_email_all(subject, f'{username}\n' + text)

    def send_email_all(self, subject, body, mailtype='plain', attachment=None):
        """  Common interface for sending mail"""
        msg = MIMEMultipart()  
        msg["Subject"] = Header(subject, "utf-8")
        msg["from"] = self.email_sender
        try:
            if len(self.email_recipients):
                msg['To'] = self.email_recipients
                msg.attach(MIMEText(body, mailtype, 'utf-8'))
                if attachment:  # If there is any attachment
                    with open(attachment, 'rb') as f:
                        mime = MIMEBase('text', 'txt', filename=attachment)
                        mime.add_header('Content-Disposition', 'attachment', filename=f'{self.name}.docx')
                        mime.set_payload(f.read())
                        encoders.encode_base64(mime)
                        msg.attach(mime)
                self.smtp.sendmail("xulei2412@foxmail.com", msg['To'], msg.as_string())
                self.smtp.quit()
            else:
                print('No recipients!')
        except smtplib.SMTPException as e:
            print(e)


