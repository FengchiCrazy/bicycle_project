#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  clean_for_traffic.py
#         Author @  Fengchi
#    Create date @  2017-01-09 22:42:49
#  Last Modified @  2017-01-11 12:20:22
#    Description @  
# *************************************************************

import datetime
import os
import pdb

DATA_PATH    = '/home/dongfengchi/bicycle_data/NYC/data'
WEATHER_DATA = '/home/dongfengchi/bicycle_data/NYC/weather_data_NYC.csv'
TIME_FORMAT1 = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT2 = "%m/%d/%Y %H:%M"
TIME_FORMAT3 = "%m/%d/%Y %H:%M:%S"


def remove_quote(string):
    if len(string) < 1:
        return string
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

def get_weather_data(weather_data = WEATHER_DATA, start_date = '2013-07-01', end_date = '2016-09-30'):
    from collections import OrderedDict


    WEATHER_DATE_FORMAT = "%Y-%m-%d"
    start_date_dt = datetime.datetime.strptime(start_date, WEATHER_DATE_FORMAT)
    end_date_dt   = datetime.datetime.strptime(end_date, WEATHER_DATE_FORMAT)
    with open(weather_data) as data:
        res = OrderedDict()
        header = data.readline()
        date_last = None

        data_list = [
            'max_temp',
            'min_temp',
            'max_wind_speed',
            'min_wind_speed',
            'total_rain',
        ]

        max_temp = -100.0
        min_temp = 100.0
        max_wind_speed = -1.0
        min_wind_speed = 1000
        total_rain = 0.0
        for line_ in data:
            line = line_.strip().split(',')
            date = datetime.datetime.strptime(line[0], WEATHER_DATE_FORMAT)
            if date < start_date_dt or date > end_date_dt:
                continue

            if date_last != date:
                day_dict = {}
                for item in data_list:
                    day_dict[item] = eval(item)

                res[date] = day_dict

                # init
                max_temp = -100.0
                min_temp = 100.0
                max_wind_speed = -1.0
                min_wind_speed = 1000
                total_rain = 0.0
            
            
            temp_ = line[2]
            if temp_ == "-9999":
                continue
            temp = float(temp_)

            wind_speed_ = line[8]
            if wind_speed_ == "Calm" or wind_speed_ == "-9999.0":
                wind_speed = 0.0
            else:
                wind_speed = float(wind_speed_)

            rain_vol_ = line[10]
            if rain_vol_ == 'N/A':
                rain_vol = 0.0
            else:
                rain_vol = float(rain_vol_)

            if temp > max_temp:
                max_temp = temp
            if temp < min_temp:
                min_temp = temp
            if wind_speed > max_wind_speed:
                max_wind_speed = wind_speed
            if wind_speed < min_wind_speed:
                min_wind_speed = wind_speed
            total_rain += rain_vol

    return res, data_list


if __name__ == "__main__":
    final_data, data_list = get_weather_data()
    print('weather data finished!')
    #print(weather_data)
    
    #data_dict = get_data_collection()

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
             
                try:
                    rent_time_dt = datetime.datetime.strptime(rent_time, TIME_FORMAT1)
                except:
                    try:
                        rent_time_dt = datetime.datetime.strptime(rent_time, TIME_FORMAT2)
                    except:
                        rent_time_dt = datetime.datetime.strptime(rent_time, TIME_FORMAT3)
                year = rent_time_dt.year
                month = rent_time_dt.month
                day   = rent_time_dt.day

                date_ = datetime.datetime(year, month, day)

                if 'count' not in final_data[date_]:
                    final_data[date_]['count'] = 0
                final_data[date_]['count'] += 1
                

            print('%s finished!' % file_name)

    fw = open("pred.csv", "w")
    data_list.append('count')
    for key, dict_ in final_data.items():
        to_write = [key.year, key.month, key.day]
        for item in data_list:
            to_write.append(dict_.get(item, 'NA'))
        fw.write(','.join([str(x) for x in to_write]) + '\n')
    fw.close()

            
            

        
