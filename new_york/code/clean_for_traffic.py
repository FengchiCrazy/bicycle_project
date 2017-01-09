#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  clean_for_traffic.py
#         Author @  Fengchi
#    Create date @  2017-01-09 22:42:49
#  Last Modified @  2017-01-09 23:50:43
#    Description @  
# *************************************************************

import datetime
import os
import pdb

DATA_PATH = '/home/dongfengchi/bicycle_data/NYC/data'

def remove_quote(string):
    if string[0] == '"':
        return string[1:-1]
    return string

for file_name in os.listdir(DATA_PATH):
    with open(DATA_PATH + os.sep + file_name) as data:
        for line_ in data:

        
