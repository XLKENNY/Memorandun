# -*- coding:utf-8 -*-
# memorandum
# main.py
# author: KENNY

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import MariaDB_operator, welcome, log_ctrl, mkconf


class run_main():
    def __init__(self, root_logger, config):
        self.root_logger = root_logger
        self.config = config

    def login(self):
        """ Login: 
            returns the name if login is successful,
            If login fails to prompt for registration,
            If you register, call the register function,
            Otherwise, False is returned
        """
        user_id, user_name = welcome.login(self.root_logger, self.config)
        if(not user_id):
            choice = input('register[y/n]?').upper()
            if (choice == 'Y'):
                user_id, user_name = self.register()
        return user_id, user_name

    def register(self):
        """ Registration:
            Successful registration prompts whether to log in or not,
            False is returned when not logged in, 
            the user's id and name are returned when successfully logged in
        """
        if(welcome.register(self.root_logger, self.config)):
            choice = input('login[y/n]?').upper()
            if (choice == 'Y'):
                id, name = welcome.login(self.root_logger, self.config)
                return id, name
            return False, False

    def run_normal_menu(self):
        """Register login menu"""
        user_id, user_name = self.login()
        if(user_id):
            self.run_loading(user_id, user_name)

    def run_loading(self, user_id, user_name):
        """log in successfully"""
        admin = MariaDB_operator.Operator(user_id, user_name)
        while True:
            # Menu interface after successful login
            choice_w = welcome.welcome(user_id, user_name)
            # Display all items
            if (choice_w == 1):
                admin.show_record()
            # Add a memo
            elif (choice_w == 2):
                admin.add_record()
            # Delete a memo
            elif (choice_w == 3):
                admin.delete_record()
            # modify a memo
            elif (choice_w == 4):
                admin.modify_record()
            # Export to Word file
            elif (choice_w == 5):
                admin.export2word()
            # Send a email
            elif (choice_w == 6):
                admin.send_email()
            # Exit this program
            elif (choice_w == 7):
                print("Thank you for your time!bye")
                self.root_logger.info(f'{user_name} has been log out')
                return False
            # MModify permissions for other users if you are an administrato
            elif (choice_w == 8):
                self.config.change_operation() 
            input("press enter to continue:")
        return admin


def main():
    config = mkconf.ConfigAdmin()  # 配置文件
    root_logger = log_ctrl.memo_log()  # 日志
    run_admin = run_main(root_logger, config)
    run_admin.run_normal_menu()


if __name__ == "__main__":
    main()
