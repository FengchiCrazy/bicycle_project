#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  count_stations.py
#         Author @  Fengchi
#    Create date @  2017-01-12 10:19:05
#  Last Modified @  2017-01-14 10:43:27
#    Description @  
# *************************************************************

import os
import datetime
from collections import OrderedDict

DATA_DIR = '/home/dongfengchi/bicycle_data/NYC/data'
TIME_FORMAT1 = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT2 = "%m/%d/%Y %H:%M"
TIME_FORMAT3 = "%m/%d/%Y %H:%M:%S"

NA = "NA"

def _remove_quote(string):
    if len(string) < 1:
        return ''
    if string[0] == '"':
        return string[1:-1]
    return string

def get_month_station(write_file = 'station_count.csv'):
    fw = open(write_file, 'w')
    for file_name in sorted(os.listdir(DATA_DIR)):
        #print(file_name)
        stations_set = set()
        with open(DATA_DIR + os.sep + file_name) as data:
            header = data.readline()
            
            for line_ in data:
                line = line_.strip().split(',')
                stations_set.add(line[3])
            
            if file_name[4] == '-':
                fw.write(file_name[:7])
            else:
                fw.write(file_name[:4] + '-' + file_name[4:6])
            fw.write(',' + str(len(stations_set))  + ',' + '|'.join([str(x) for x in list(stations_set)])+ '\n')
            print(file_name + ' finished!')

def get_daily_station(write_file = 'daily_station_count.csv'):
    fw = open(write_file, 'w')
    ret = OrderedDict()
    for file_name in sorted(os.listdir(DATA_DIR)):
        #print(file_name)
        with open(DATA_DIR + os.sep + file_name) as data:
            header = data.readline()
            header = header.strip().split(',')
            
            header_index = {}
            for idx, column in enumerate(header):
                header_index[_remove_quote(column)] = idx   
            
            #print(header_index)
            for line_ in data:
                line = [_remove_quote(x) for x in line_.strip().split(',')]
                
                rent_time = line[header_index['starttime']]
                start_station_id = line[header_index['start station id']]
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
                
                day_dt = datetime.datetime(year, month, day)
                
                if (day_dt, start_station_id) not in ret:
                    ret[(day_dt, start_station_id)] = 0
                ret[(day_dt, start_station_id)] += 1

            print(file_name + ' finished!')
    
    stations_set = set()
    dates_set = set()
    for key, count in ret.items():
        dates_set.add(key[0])
        stations_set.add(key[1])

    dates_indexes = sorted(list(dates_set))
    stations_columns = sorted(list(stations_set))
    
    fw.write(',' + ','.join(stations_columns) + '\n')
    for date in dates_indexes:
        to_write = []
        for station in stations_columns:
            to_write.append(ret.get((date, station), 0))
        fw.write(date.strftime('%Y-%m-%d') + ',')
        fw.write(','.join(str(x) for x in to_write) + '\n')
    
if __name__ == "__main__":
    #get_month_station()    
    get_daily_station()
