# -*- coding:utf-8 -*-
# mkconf.py
# memorandum
# author: kenny
import os
import sys
import re
import json
import configparser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from . import welcome


class ConfigAdmin():
    """Operate on the configuration file"""
    def __init__(self):
        self.config_path = os.path.join(BASE_DIR, 'conf', 'common.ini')  # 配置文件所在目录
        self.check_config()

    def check_config(self):
        """Checks if there is a configuration file: 
              if there is a configuration file, returns true
              If there is no configuration file, create a new default and return false
        """
        config = configparser.ConfigParser()
        if(not os.path.exists(self.config_path)):
            self.add_config('00000', 'admin', 'admin', ['1', '2', '3', '4', '5', '6', '7', '8'])
            return False
        return True

    def add_config(self, section, name, password, op=['7'], enable='1'):
        """Add profile information: section is the user id
           If an id already exists, it cannot be added
        """
        try:
            config = configparser.ConfigParser()
            config.read(self.config_path)
            
            # Write to configuration file
            config[section] = {}
            config[section]['user_file'] = os.path.join(BASE_DIR, 'db', f'{section}.json')
            config[section]['log_file'] = os.path.join(BASE_DIR, 'log', f'{section}.log')
            with open(self.config_path, 'w') as f:
                config.write(f)
            
            # Write to json file
            d = {
                    'username': name,
                    'password': password,
                    'operation': op,
                    'enabled': enable
                }
            with open(config[section]['user_file'], 'w') as f:
                json.dump(d, f)
            return True
        except Exception as e:
            print(e)
            return False

    def find_config(self, section):
        """Find the Password for the configuration information for the user name based on the id，
            If NO section is found, output NO USER
        """
        try:
            config = configparser.ConfigParser()
            # Determine if the configuration file exists
            if(os.path.exists(self.config_path)):
                config.read(self.config_path)
                # Determine if the user exists
                if (config.has_section(section)):
                    with open(config[section]['user_file'], 'r') as f:
                        info = json.load(f)
                    # Determine if the user is on the blacklist
                    if(info['enabled'] == '1'):
                        return info['password']
                    else:
                        print('YOUR ARE IN BALCKLISTED!')
                else:
                    print('NO USER !')
            else:
                print('NO FILE')
            return False
        except Exception as e:
            print(e)
            return False

    def change_operation(self):
        """Administrator adds user permissions"""
        try:
            config = configparser.ConfigParser()
            user_id = input('Please input the userid:').strip(' ')
            config.read(self.config_path)
            if(user_id != 'admin' and config.has_section(user_id)):
                print('user is exist:')
                enable = input('Whether to be blacklisted[0/1]?[0] is blacklisted:').strip(' ')
                if(enable == '1'):
                    """Not blacklisted, you can set permissions"""
                    for key, value in welcome.menu_dict.items():
                        print(f'{key} : {value}')
                    operator_in = input('Please enter all the number of operation one time:').strip(' ')
                    operator_set = set(re.findall('[1-6]', operator_in)) 
                    operator_set.add("8")
                    operator = list(operator_set)
                    operator.sort()
                else:
                    operator = "[0]"
                with open(config[user_id]['user_file'], 'r') as f:
                    info = json.load(f)
                password = info['password']
                name = info['username']
                self.add_config(user_id, name, password, operator, enable)
                print('add successful!')
                return True
            else:
                print('No user,Please enter the correct username!')
        except Exception as e:
            print(e)
        return False

    def find_sections(self):
        """Returns all sections of the configuration file"""
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config.sections()

    def find_name(self, section):
        """ Return username"""
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if config.has_section(section):
            with open(config[section]['user_file'], 'r') as f:
                info = json.load(f)
            return info['username']
        else:
            print('find name error')
            return False

    def find_email(self, section):
        """Returns the user's email address"""
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if config.has_section(section):
            with open(config[section]['user_file'], 'r') as f:
                info = json.load(f)
            return info['username']
        else:
            print('find name error')
            return False
