#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  count_stations.py
#         Author @  Fengchi
#    Create date @  2017-01-12 10:19:05
#  Last Modified @  2017-01-12 10:29:56
#    Description @  
# *************************************************************

import os

fw = open('stations_count', 'w')
for file_name in sorted(os.listdir('data/')):
    #print(file_name)
    stations_set = set()
    with open('data/' + file_name) as data:
        header = data.readline()
        
        for line_ in data:
            line = line_.strip().split(',')
            stations_set.add(line[3])
        
        if file_name[4] == '-':
            fw.write(file_name[:7] + ',' +  str(len(stations_set)) + '\n')
        else:
            fw.write(file_name[:4] + '-' + file_name[4:6] + ',' + str(len(stations_set)) + '\n')
        print(file_name + ' finished!')
        
    
