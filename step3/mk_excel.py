# -*- coding:utf-8 -*-
from collections import defaultdict
import xlwt
import datetime
import numpy as np
import pdb

data_file = '../derived/rent_net_data'
target_list_file = '../derived/net_id_ll.csv'
#target_list = ['1028', '6117']
target_list = []
with open(target_list_file, 'r') as ftl:
    # header
    line = ftl.readline()
    while line:
        line = ftl.readline()
        text = [x.strip() for x in line.strip().split(',') if x ]
        if len(text) < 1:
            break
        target_list.append(text[0])

print target_list
print len(target_list)
fd = open(data_file, 'r')
res = defaultdict(list)

def time_handle(sec_str):
    '''
    handle the the time to %H%M%S
    Input: the result of int everyday time in hive
    '''
    if sec_str == 'NULL':
        return None
    if len(sec_str) <= 6 and len(sec_str) >= 2:
        return (6 - len(sec_str)) * '0' + sec_str
    else:
        return None

def add_zero(x):
    return "%02d" % x

for line in fd:
    data = line.strip().split()
    net_id = data[0]
    date = data[1]
    time = time_handle(data[2])
    if time is None:
        continue
    if net_id in target_list:
        res[net_id].append(datetime.datetime.strptime((date + time), "%Y%m%d%H%M%S"))

fd.close()

f_gap = open('gap.csv', 'w')
f_count = open('count.csv', 'w')

# csv header
f_gap.write('net_id,hour,median_gap\n')
f_count.write('net_id,hour,median_count\n')
    
for net_id in target_list:
    day_gap   = defaultdict(list)
    day_count = defaultdict(lambda: defaultdict(int))
    # print res[net_id]
    f_net = open('../data/%s.csv' % net_id, 'w')
    # pdb.set_trace()
    f_net.write("%s,%s,%s,%s" % ('date', 'time', 'hour', 'gap'))
    lis_time = res[net_id]
    lis_time.sort()
    for i in range(len(lis_time) - 1):
        hour = lis_time[i].strftime("%H")
        day  = lis_time[i].strftime("%m%d")
        day_count[hour][day] += 1
        
        if lis_time[i].strftime("%m%d") == lis_time[i + 1].strftime("%m%d"):
            gap_sec = (lis_time[i + 1] - lis_time[i]).seconds
            day_gap[hour].append(gap_sec)
        else:
            gap_sec = ''
        f_net.write("%s,%s,%s,%s\n" % (lis_time[i].strftime("%Y-%m-%d"), lis_time[i].strftime("%H:%M:%S"), hour, gap_sec))
    f_net.write("%s,%s,%s,\n" % (lis_time[len(lis_time) - 1].strftime("%Y-%m-%d"), lis_time[len(lis_time) - 1].strftime("%H:%M:%S"), hour))

    hour = lis_time[len(lis_time) - 1].strftime("%H")
    day  = lis_time[len(lis_time) - 1].strftime("%m%d")
    day_count[hour][day] += 1

    hours = [add_zero(x) for x in range(6, 22)]
    for hour in hours:
        f_gap.write("%s,%s,%s\n" % (net_id, hour, np.median(day_gap[hour])))

        counts = list(day_count[hour].values())
        f_count.write("%s,%s,%s\n" % (net_id, hour, np.median(counts)))

    f_net.close()

f_gap.close()
f_count.close()

