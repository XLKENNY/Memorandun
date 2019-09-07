# linux
# Celery
# memorandum_alarm.py
# author:KENNY

import datetime
import time
from celery import Celery
from sqlalchemy import create_engine, Column, Integer, Boolean, DateTime , String, ForeignKey  
from sqlalchemy.orm import sessionmaker, relationship 
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy_utils import database_exists, create_database  
from sqlalchemy import and_
import send_email


# Create app
app = Celery("memorandum_alarm", broker="amqp://", backend="redis://localhost")
app.config_from_object("config")

Base = declarative_base()

class Users(Base):
    """User information data sheet"""
    __tablename__ = "users"

    user_id = Column('user_id', String(10), primary_key=True, nullable=False)
    user_name = Column('user_name', String(20), nullable=False)
    email = Column("email", String(20))


class Things(Base):
    """Memo information data sheet"""
    __tablename__ = "things"

    thing_id = Column("thing_id", Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column("content", String(100))
    alarm_date = Column("alarm_date", DateTime)
    is_alarm = Column('is_alarm', Boolean)
    user_id = Column(String(10), ForeignKey("users.user_id"))
    user = relationship("Users", back_populates="thing")
Users.thing = relationship('Things', back_populates='user')

@app.task
def worker(name):
    """task"""
    print(f"{name} is working!")
    try :
        data_user='root'
        data_psw="kenny12345"
        data_hostip='192.168.8.142'
        data_base='memorandum'
        engine = create_engine(f'mysql+pymysql://{data_user}:{data_psw}@{data_hostip}/{data_base}')
        Base.metadata.create_all(bind=engine)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        print('database is linking!')
        text_dict = {}
        for i in session.query(Things).filter(Things.alarm_date > datetime.datetime.now(),Things.alarm_date < (datetime.datetime.now() + datetime.timedelta(seconds=60)),Things.is_alarm==0).all():
            if (i.user_id in text_dict):
                text_dict[i.user_id]['content'].append(i.content)
            else:
                text = {}
                text['content'] = [i.content]
                text['name'] = i.user.user_name
                text['email'] = i.user.email
                text_dict[i.user_id] = text
            i.is_alarm = 1
            session.commit()
        if(text_dict):
            send_alarm_email(text_dict)
    except Exception as e:
        print(e)
        return False
    return f'{name}-10s-ok'

def send_alarm_email(text_dict):
    """If there is a reminder message, send an email"""
    try:
        for key, value in text_dict.items():
            user_id = key
            user_name = value['name']
            email_address = value['email']
            content = str(value['content'])
            mail = send_email.MailMaster(user_id, email_address=email_address, password=send_email.get_password(), name=user_name)
            mail.send_email_all(f'Hello{user_name},Remind you to do these things！', content)
            print('sending email successful')
    except Exception as e:
        print('sending email failed:', e)

