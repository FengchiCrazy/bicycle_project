# -*- coding:utf-8 -*-

import datetime
import pandas as pd
import numpy as np
import os
import pdb

# parameter 
FILE_DIR = "/Users/fengchi/Documents/bicycle_data/"
CLUSTER_RESULT = "cluster_result.csv"
START_DATE = "20130813"
END_DATE   = "20131113" 

#bike1_num_dict = {
#    '3655': 1,
#    '3656': 2,
#    '3671': 3,
#    '3661': 4,
#    '3644': 5,
#    '3648': 6,
#    '3657': 7,
#    '3642': 8,
#    '3643': 9,
#    '3607': 10,
#    '3603': 11,
#    '3606': 12,
#    '3604': 13,
#    '3605': 14,
#    '3647': 15,
#}

net_cluster_dict = {}
with open(CLUSTER_RESULT) as data:
    header = data.readline()
    for line_ in data:
        line = line_.strip().split(',')
        netid     = line[0]
        clusterid = line[1]
        
        net_cluster_dict[netid] = clusterid
#pdb.set_trace()

# 因为时间格式有时会缺失0，不是HHMMSS的规范时间格式
# 所以需要再时间格式前补零
def pad_time_zero(string):
	return (6 - len(string)) * '0' + string

hour_range = [str(x) for x in range(5, 22)]

# date range
start_date_dt = datetime.datetime.strptime(START_DATE, "%Y%m%d")
end_date_dt   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
time_delta    = datetime.timedelta(days=1)

date_range = []
tmp_dt = start_date_dt
while tmp_dt <= end_date_dt:
    date_range.append(tmp_dt)
    tmp_dt += time_delta

# row keys and column keys
row_key = [x.strftime("%m%d") + '-' + y for x in date_range for y in hour_range]
column_key = [str(x) + '-' + str(y) for x in range(1, 21) for y in range(1, 21)]

# create a zero dataframe
zero_matrix = np.zeros((len(row_key), len(column_key)), dtype = np.int)
df = pd.DataFrame(zero_matrix, index = row_key, columns = column_key)
row_key_set = set(row_key)

for file_name in os.listdir(FILE_DIR):
    if file_name[:5] != 'trans':
        continue

    with open(FILE_DIR + file_name, 'r') as data:
        # handle header
        line_ = data.readline()
        i = 0
        while True:
            line_ = data.readline()
            line  = line_.strip().split(',')
            if len(line) <= 1:
                break

            rent_netid   = line[1]
            return_netid = line[8]
            #pdb.set_trace()
            
            # 判断借还站点是否在给定的站点列表中
            if rent_netid not in net_cluster_dict or return_netid not in net_cluster_dict:
                continue
            

            # 根据原始文件行列的相对位置提取出借车时间和日期
            # 0为第一列
            rent_date = line[2]
            rent_time = line[3]

            rent_date_dt = datetime.datetime.strptime(rent_date, "%Y%m%d")
            if rent_date_dt < start_date_dt or rent_date_dt > end_date_dt:
                continue
                
            try:
                rent_clusterid = net_cluster_dict[rent_netid]
                return_clusterid = net_cluster_dict[return_netid]
            except:
                pdb.set_trace()
            net_key = str(rent_clusterid) + '-' + str(return_clusterid)
            
            hour = datetime.datetime.strptime(pad_time_zero(rent_time), "%H%M%S").strftime("%H")

            # 把05转换成5
            hour = str(int(hour))

            time_key = rent_date[4:] + '-' + hour
            if time_key in row_key_set:
                df.loc[time_key, net_key] += 1
        
            if i % 100000 == 0:
                print(file_name + ':' + str(i) + '  lines')
            i += 1

    print(file_name)

#save result
df.to_csv("result_all.csv")
