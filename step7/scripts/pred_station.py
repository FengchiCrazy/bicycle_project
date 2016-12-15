#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#       Filename @  pred_station.py
#         Author @  Fengchi
#    Create date @  2016-12-14 20:15:48
#  Last Modified @  2016-12-14 20:41:06
#    Description @  
# *************************************************************

import os
import sys

DATA_DIR = '/home/dmc/project/bike/'

def get_max_station():
    from collections import defaultdict

    rent_station_count = defaultdict(int)

    for data_file in sorted(os.listdir(DATA_DIR)):
        if data_file[:4] != 'tran':
            continue

        with open(DATA_DIR + data_file) as data:
            # header
            header = data.readline()
            for line_ in data:
                line = line_.strip().split(',')
                rent_netid = line[1]
                rent_station_count[rent_netid] += 1

        print(data_file + " Finished!!")
                

    res_count = sorted(rent_station_count.items(), key = lambda x: x[1], reverse = True)

    print(res_count[:10])


            
        



