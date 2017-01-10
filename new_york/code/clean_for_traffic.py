#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  clean_for_traffic.py
#         Author @  Fengchi
#    Create date @  2017-01-09 22:42:49
#  Last Modified @  2017-01-10 11:08:24
#    Description @  
# *************************************************************

import datetime
import os
import pdb

DATA_PATH = '/home/dongfengchi/bicycle_data/NYC/data'
TIME_FORMAT1 = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT2 = "%m/%d/%Y %H:%M"


def remove_quote(string):
    if string[0] == '"':
        return string[1:-1]
    return string

def get_data_collection():
    from collections import OrderedDict

    data_dict = OrderedDict()

    years     = range(2013, 2017)
    months    = range(1, 13)
    subsciber = ['0', '1']
    ages      = list(range(10, 71, 10)) + ['>70', 'NA']
    genders   = ['M', 'F', 'NA']

    # init data_dict
    for year in years:
        for month in months:
            for sub in subsciber:
                for age in ages:
                    for gender in genders:
                        key = tuple([str(x) for x in [year, month, sub, age, gender]])
                        data_dict[key] = 0
    return data_dict

data_dict = get_data_collection()
#pdb.set_trace()

for file_name in os.listdir(DATA_PATH):
    with open(DATA_PATH + os.sep + file_name) as data:
        header_ = data.readline()
        header = header_.strip().split(',')
        
        header_index = {}
        for idx, column in enumerate(header):
            header_index[remove_quote(column)] = idx   
        
        for line_ in data:
            line = [remove_quote(x) for x in line_.strip().split(',')]
            
            rent_time = line[header_index['starttime']]
            user_type = line[header_index['usertype']]
            birth_year = line[header_index['birth year']]
            gender     = line[header_index['gender']]

            try:
                rent_time_dt = datetime.datetime.strptime(rent_time, TIME_FORMAT1)
            except:
                rent_time_dt = datetime.datetime.strptime(rent_time, TIME_FORMAT2)
            year = rent_time_dt.year
            month = rent_time_dt.month
            
            if user_type == 'Subscriber':
                sub = '1'

                if birth_year == "\\N":
                    age = "NA"
                else:
                    age_ = year - int(birth_year)
                    if age_ > 70:
                        age = '>70'
                    else:
                        for i in range(1, 8):
                            if age_ < i * 10:
                                age = i * 10
                                break

                # Male means 1
                if gender == "1":
                    gend = "M"
                elif gender == "2":
                    gend = "F"
                else:
                    gend = "NA"
            else:
                # Customer
                sub = '0'
                age = "NA"
                gend = "NA"

            key = tuple([str(x) for x in [year, month, sub, age, gend]])
            data_dict[key] += 1

        print('%s finished!' % file_name)

fw = "describe.csv"
for key, cnt in data_dict.items():
    fw.write(','.join(list(key) + list(str(cnt))) + '\n')
fw.close()

            
            

        
