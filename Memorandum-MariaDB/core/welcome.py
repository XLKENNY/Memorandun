# -*- coding:utf-8 -*-
# memorandum
# welcome.py
# author: KENNY

import random
import string
import pickle
import os
import json
from . import log_ctrl, mkconf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_file = os.path.join(BASE_DIR, 'conf', 'common.ini')
# Main course list
menu_dict = {
    '[1]': 'show the items',
    '[2]': 'add the item',
    '[3]': 'delete the item',
    '[4]': 'modify the item',
    '[5]': 'export the file',
    '[6]': "send a email",
    '[7]': 'leave the program',
    '[8]': "change user's operation"
}


s = "****************"


def welcome(userid, username):
    """The main menu displays a welcome message"""
    print("\nThis is a memorandum!".center(30))
    print(f'HELLO {username} \n')
    json_path = os.path.join(BASE_DIR, 'db', f'{userid}.json')
    with open(json_path, 'r') as f:
        d = json.load(f)
    for key in d['operation']:
        if(key != ','):
            print(f'[{key}] : ', end ='')
            print(menu_dict[f'[{key}]'])
    choice = input("Please enter your choice:").strip(' ')
    if (choice in d['operation']):
        return int(choice)
    else:
        print('Please enter correct number:')


def login(logger, config):
    """Login"""
    if(os.path.exists(common_file)):
        print(s + "Log-in" + s)
        num = 0
        while num < 3:
            num += 1
            user_id = input("Please input your id:").strip(' ')
            Password = input("Please input your password:").strip(' ')
            if(config.find_config(user_id) == Password):
                print("Congratulations, landing......")
                name = config.find_name(user_id)
                logger.info(f'{name} has been login')
                return user_id, name
            if(num != 3):
                print("Sorry!your Landing is error,you have %s chances"% (3-num)) 
                logger.error('login failure because error enter!')
        print("sorry,your chances are exhausted!")
        logger.error('login failure because the chances are exhausted!')
    else:
        print('NO USER!')
        logger.error('There has no user!')
    return False, False


def create_id(users_id):
    """Generate a 10-digit numeric id"""
    while True:
        idd = ''
        for i in range(10):
            letter = random.choice(string.digits)
            idd += letter
        if idd not in users_id:
            return idd


def register(logger, config):
    """Register"""
    if(os.path.exists(common_file)):
        print(s + "注册" + s)
        users_id = config.find_sections()
    else:
        users_id = {}
    try:
        user_id = create_id(users_id)  # Generate random id
        User_name = input("Please input your name that you want to register:").strip(' ')
        User_Password = input("Please input your password that you want to register:").strip('')
        if(User_name and User_Password):
            if(config.add_config(user_id, User_name, User_Password)):
                logger.info(f'{User_name} register successful!')
                print('registration complete')
                print(f'Your id is: {user_id}')
                return int(user_id)
            else:
                print('registration failed!')
                logger.info(f'{User_name} register failed!')
                return False
        else:
            logger.error(f'{User_name} has failed to register because of the blank name')
            print('username and userpassword can not be empty ')
        return False
    except Exception as e:
        print(e)
        logger.error(f'{User_name} has failed to register!')
        return False
