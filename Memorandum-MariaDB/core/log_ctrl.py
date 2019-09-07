# -*- coding:utf-8 -*-
# memorandum
# log_ctrl.py
# author: kenny

import logging
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Disable all log output
tap = input('writing to the log[y/n]?').strip(' ').upper()
if(tap == 'N'):
    logging.disable(logging.CRITICAL)


def memo_log(logger_name='ROOT-LOG', log_file=os.path.join(BASE_DIR, 'log', 'root.log'), level=logging.DEBUG):
    # Create a logger object
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 添加等级

    # Create the logger object creation console: console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Create log_file :handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')

    # Create the formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

    # Add the formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add ch, fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
