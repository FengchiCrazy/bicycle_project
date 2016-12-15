#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  model_prepare_for_32.py
#         Author @  Fengchi
#    Create date @  2016-12-14 14:31:15
#  Last Modified @  2016-12-14 21:59:22
#    Description @  
# *************************************************************

import os
import sys
import datetime
from collections import defaultdict
import pdb

FILE_NAME = "../data/xiasha_trans.csv"
DATA_DIR  = '/home/dmc/project/bike/'
START_DATE = '20130902'
END_DATE   = '20130929'
START_DATE_DT = datetime.datetime.strptime(START_DATE, "%Y%m%d")
END_DATE_DT   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
MIN_HOUR   = 5
MAX_HOUR   = 22

def get_dict():
    hour_range = range(0, 24)

# date range
    start_time = datetime.datetime.strptime(START_DATE, "%Y%m%d")
    end_time   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
    time_delta = datetime.timedelta(days=1)

    date_range = []
    while start_time <= end_time:
        date_range.append(start_time)
        start_time += time_delta

    keys = [d.strftime('%m%d') + '_' + str(h) for h in hour_range for d in date_range]

    count_dict = dict([(key, 0) for key in keys])

    return count_dict


def counter():
    count_dict = get_dict()
    for data_file in sorted(os.listdir(DATA_DIR)):
        if data_file[:4] != 'tran':
            continue
    
        with open(DATA_DIR + data_file, 'r') as data:
            line_ = data.readline()
            while True:
                line_ = data.readline()
                line  = line_.strip().split(",")
                if len(line) <= 1:
                    break
                
                rent_netid = line[1]
                if rent_netid != '4051':
                     continue

                date_dt = datetime.datetime.strptime(line[2], "%Y%m%d")
                if date_dt < START_DATE_DT or date_dt > END_DATE_DT:
                    continue

                date = line[2][4:]
                hour = str(int(line[3][:2]))
             
                key = date + '_' + hour
                count_dict[key] += 1
    
        print(data_file + " Finished!!")
    return count_dict
        
    
read_file_name = "weather_output.csv"
target_file_name = "model_4051.csv"

fw = open(target_file_name, 'w')

with open(read_file_name, 'r') as data:
    count_dict = counter()
    line_ = data.readline()
    fw.write("date,weekday,hour,temp,sunny,wind_speed,count\n")
    
    while True:
        line_ = data.readline()
        line  = line_.strip().split(',')
        if len(line) <= 1:
            break
        
        key = line[0]

        if key not in count_dict:
            count = 0
        else:
            count = count_dict[key]
        
        date = '2013' + line[0].split("_")[0]
        hour = line[0].split("_")[1]
        if int(hour) <= MIN_HOUR or int(hour) >= MAX_HOUR:
            continue
        weekday = line[1]
        temp = line[2]
        wind_speed = line[3]
        sunny = line[4]
        
        out_list = [date, str(weekday), hour, temp, sunny, wind_speed, str(count)]
            
        
        fw.write(','.join(out_list) + '\n')

fw.close()




