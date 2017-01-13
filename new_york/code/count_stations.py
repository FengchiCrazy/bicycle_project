#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  count_stations.py
#         Author @  Fengchi
#    Create date @  2017-01-12 10:19:05
#  Last Modified @  2017-01-13 20:58:48
#    Description @  
# *************************************************************

import os

DATA_DIR = '/home/dongfengchi/bicycle_data/NYC/data'

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
        
    
if __name__ == "__main__":
    get_month_station()    
