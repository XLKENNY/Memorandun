# -*- coding:utf-8 -*-
# memorandum
# connect_database
# author: KENNY

import os
import sys
import time
import json
from sqlalchemy import create_engine, Column, Integer, DateTime ,Boolean, String, ForeignKey  
from sqlalchemy.orm import sessionmaker, relationship  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database  
from sqlalchemy import and_
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import time_converter, log_ctrl

Base = declarative_base()


class Users(Base):
    """User data sheet"""
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
    is_alram = Column('is_alarm', Boolean)
    user_id = Column(String(10), ForeignKey("users.user_id"))
    user = relationship("Users", back_populates="thing")
Users.thing = relationship('Things', back_populates='user')


class DataOperator():
    """Operational database"""
    def __init__(self, user_id, user_name):
        self.session = self.connect_database()
        self.user_id = user_id
        self.user_name = user_name

    def connect_database(self, data_user='root', data_psw="xxxxx", data_hostip='localhost', data_base='memorandum'):
        """Connect to database"""
        # data_user = input("Please enter a database user name:")
        # data_psw = input("Please enter the database password:")
        # data_hostip = input("Please enter the database host[localhost]:")
        # data_base = input("Please enter a database name:")
        try :
            if not database_exists(f'mysql+pymysql://{data_user}:{data_psw}@{data_hostip}/{data_base}'):
                create_database(f'mysql+pymysql://{data_user}:{data_psw}@{data_hostip}/{data_base}')
            engine = create_engine(f'mysql+pymysql://{data_user}:{data_psw}@{data_hostip}/{data_base}')
            Base.metadata.create_all(bind=engine)
            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            print('database is linking!')
            return session
        except Exception as e:
            print(e)
            return False
    
    def change_time(self, change_time):
        """Format reminder time"""
        temp_date = time_converter.ChangeTime(change_time)
        temp_date.time_change_cn()
        temp_date.time_add()
        temp_date.time_change_f()
        return temp_date.dt

    def add_record(self,content, alarm_date, logger):
        """Add a memo"""
        if self.session:
            try:
                thing = Things()
                thing.user_id = self.user_id
                thing.content = content
                thing.alarm_date = self.change_time(alarm_date)
                thing.is_alram = False
                user = self.session.query(Users).filter(Users.user_id == thing.user_id).all()
                if not user:
                    user = Users()
                    user.user_id = self.user_id
                    user.user_name = self.user_name
                    user.email = input('Please enter your email:').strip('')
                    thing.user = user
                    self.session.add(user)
                self.session.add(thing)
                self.session.commit()
                print('add ok1')
                logger.info(f'{self.user_name} has add a memo successed!')
                return True
            except Exception as e:
                print(e)
                logger.info(f'{self.user_name} has add a memo failed!')
                return False
        else:
            print('No session!')
            logger.info(f'{self.user_name} has add a memo failed!')
            return False

    def delete_record(self, thing_id, logger):
        """Delete a memo"""
        try:
            self.session.query(Things).filter(Things.thing_id == int(thing_id)).delete()
            self.session.commit()
            print("delete ok！")
            logger.info(f'{self.user_name} has delete a memo successed!')
            return True
        except Exception as e:
            print(e)
            print("delete failed!")
            logger.info(f'{self.user_name} has delete a memo failed!')
            return False

    def show_records(self, logger):
        """SDisplay all memos"""
        length = 0
        for i in self.session.query(Things).filter(Things.user_id == self.user_id).all():
            print(f'id:{i.thing_id}  thing：{i.content}   time: {i.alarm_date}')
            length += 1
        print(f'hello {self.user_name}! you have {length} items to do!')
        logger.info(f'{self.user_name} has show the memos successed!')

    def modify_record(self, thing_id, modify_key, modify_value, logger):
        """Modify a memo"""
        try:
            if modify_key in ["content", "alarm_date"]:
                self.session.query(Things).filter(Things.thing_id == int(thing_id)).update({f'{modify_key}': f'{modify_value}'})
                self.session.commit()
                print("modify ok！")
                logger.info(f'{self.user_name} has modify a memo successed!')
                return True
            else:
                print("modify failed！please input correct modify_key")
                logger.info(f'{self.user_name} has modify a memo failed!')
                return False
        except Exception as e:
            print(e)
            logger.info(f'{self.user_name} has modify a memo failed!')
            return False

    def return_email(self):
        """Return email address"""
        try:
            info = self.session.query(Users).filter(Users.user_id == self.user_id).all()[0]
            return info.email
        except Exception as e:
            print(e)
            return False

    def return_memos(self):
        """Returns all memos for the specified id"""
        memo_list = []
        for i in self.session.query(Things).filter(Things.user_id == self.user_id).all():
            memo_list.append(f'备忘id:{i.thing_id}  备忘事项：{i.content}   提醒时间: {i.alarm_date}')
        return memo_list
