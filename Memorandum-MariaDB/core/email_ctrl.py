# -*- coding:utf-8 -*-
# email_ctrl.py
# memorandum
# author: KENNY

import smtplib
import pickle
import os
import sys
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from . import log_ctrl, connect_database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_password():
    """return  password"""
    password = 'xxxxxxxx'  # Sender's mailbox authorization code
    return password


class MailMaster:
    """Operating a mailbox"""
    def __init__(self, id, password, name, smtp_server='smtp.qq.com', email_addr='xxxxxx@xxx.com'):
        # email_addr:Sender's mailbox
        self.data_oper = connect_database.DataOperator(id, name)
        self.smtp = SMTP_SSL(smtp_server)
        self.smtp.ehlo(smtp_server)
        self.smtp.login(email_addr, password)
        self.email_sender = email_addr
        self.email_recipients = []  # Recipient's mailbox
        self.logger_email = log_ctrl.memo_log('EMAIL-LOG', os.path.join(BASE_DIR, 'log', 'email.log'))
        self.name = name  # Name of recipient

    def read_email_recipients(self):
        """Read the user's mailbox from the database"""
        try:
            self.email_recipients = self.data_oper.return_email()
        except Exception as e:
            print(e)

    def notice(self, username, text, subject='Memorandum'):
        """An email that sends notification information，
            Only the text without attachments
        """
        self.send_email_all(subject, f'{username}\n' + text)

    def send_email_all(self, subject, body, mailtype='plain', attachment=None):
        """  Common interface for sending mail
             You can send text and attachments
        """
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
                self.logger_email.info(f'{self.name} has send a email successful')
            else:
                print('No recipients!')
        except smtplib.SMTPException as e:
            self.logger_email.error(f'{self.name} has send a email failed')
            print(e)
