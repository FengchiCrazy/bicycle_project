import numpy as np
import pandas as pd
import datetime
import pdb

ERROR_DATE = '19900101010101'
BROKEN_TIME = 2 

car_num = []
with file('distinct_car_number', 'r') as f:
    for line in f:
        car_num.append(line.strip())

print len(car_num)

def combine_date(day_str, sec_str):
    if day_str == 'NULL' or sec_str == 'NULL':
        return ERROR_DATE
    if len(sec_str) <= 6:
        return day_str + '0' * (6 - len(sec_str)) + sec_str

def get_date(string):
    return datetime.datetime.strptime(string, "%Y%m%d%H%M%S")

res = {}
titles = []

with file('rent_eq_ret', 'r') as f:
    titles = f.readline().strip().split()
    line = f.readline()
    while line:
        line = line.strip().split()
        car_num = line[0]
        rent_day = combine_date(line[1], line[2])
        return_day = combine_date(line[3],line[4])
        if rent_day == ERROR_DATE or return_day == ERROR_DATE:
            print '*******************'+car_num+'****'+line[1]+line[2]+'***'+line[3]+line[4]+'*******************'
            line = f.readline()
            continue
            
        rent_day = get_date(rent_day)
        return_day = get_date(return_day)

        diff_seconds = (return_day - rent_day).seconds

        if diff_seconds <=  BROKEN_TIME * 60:
            if car_num not in res:
                res[car_num] = {}
                res[car_num]['count'] = 1
                res[car_num]['date'] = [return_day,]
            else:
                if return_day != ERROR_DATE or rent_day != ERROR_DATE:
                    
                    res[car_num]['count'] += 1
                    res[car_num]['date'].append(return_day)
                    
                  
            
        line = f.readline()

print len(res)

for k,v1 in res.items():
    print "%s\t%s\t%s" % (k, v1['count'], "\t".join([x.strftime('%Y-%m-%d') for x in v1['date']]))

                
                




    
