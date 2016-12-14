#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  model_prepare_for_32_new.py
#         Author @  Fengchi
#    Create date @  2016-12-14 10:59:40
#  Last Modified @  2016-12-14 14:30:43
#    Description @  
# *************************************************************

import datetime

WEATHER_FILE = "../data/hangzhou_2013_weather.csv"
START_DATE   = "20130902"
END_DATE     = "20130928"

START_DATE_DT = datetime.datetime.strptime(START_DATE, "%Y%m%d")
END_DATE_DT   = datetime.datetime.strptime(END_DATE, "%Y%m%d")

def is_sunny(string):
    if "雨" in string:
        return False
    else:
        return True

fw = open("weather_output.csv", "w")
write_list = [
    "date_key",
    "weekday",
    "temperature",
    "wind_speed",
    "sunny",
]
fw.write(",".join(write_list) + '\n')

with open(WEATHER_FILE, encoding='gb2312') as data:
    #header
    data.readline()
    for line_ in data:
        line = line_.strip().split(',')
        date_ = line[0]
        hour  = line[1].split(':')[0]
        temperature = line[2]
        wind_speed  = float(line[4])
        weather = line[5]

        date_dt = datetime.datetime.strptime(date_, "%Y-%m-%d")
        if date_dt < START_DATE_DT or date_dt > END_DATE_DT:
            continue

        date = date_dt.strftime("%m%d")
        weekday = date_dt.strftime("%w")
        sunny = "1" if is_sunny(weather) else "0"

        date_key = date + '_' + hour
        
        to_write = [
            date_key,
            weekday,
            temperature,
            wind_speed,
            sunny
        ]

        print(to_write)
        fw.write(",".join([str(x) for x in to_write]) + '\n')

fw.close()

        


        
            

        
