from time_handle_tools import time_handle, list_date
import pdb
import os
import pandas as pd
import numpy as np
import datetime

INTERVAL_MINUTES = 60
# the derived file from hive
# **the first four columns of file must be tran_time, rent_netid, return_netid, tran_date**
PARSE_FILE_NAME = 'netid_7_to_8'
PARSE_FILE = "%s%sderived%s%s" % (os.path.pardir, os.sep, os.sep, PARSE_FILE_NAME)

def get_netid_list(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        res = []
        while line:
            line = f.readline()
            line = line.strip()
            if len(line) == 0:
                break
            res.append(line)
    return res

def create_net_matrix(from_time, to_time, date_time):
    res = {}
    with open(PARSE_FILE, 'r') as f:
        #header
        line = f.readline()
        header = line.strip().split()
        while line:
            line = f.readline()
            line = line.strip().split()
            if len(line) < 1:
                break
            time = time_handle(line[0])
            rent_netid = line[1]
            return_netid = line[2]
            date_time_now = line[3]
            if date_time_now != date_time:
                continue

            # error handle
            if time is None or rent_netid == 'NULL' or return_netid == 'NULL':
                continue
                
            if time >= from_time and time <= to_time:
                if rent_netid not in res:
                    res[rent_netid] = {}
                    res[rent_netid][return_netid] = 1
                else:
                    if return_netid not in res[rent_netid]:
                        res[rent_netid][return_netid] = 1
                    else:
                        res[rent_netid][return_netid] += 1

    return res
            
def draw_matrix(res_dic, net_list, csv_name, file_path=None):
    #zero_arr = np.zeros((len(net_list),len(net_list)), dtype=np.int)
    if file_path:
        fw = open('%s%s%s.csv' % (file_path, os.sep, csv_name), 'w')
    else:
        fw = open('%s.csv' % csv_name, 'w')
    fw.write("%s\t%s\t%s\n"% ('rent_netid', 'return_netid', 'count'))
    for rent_netid, return_netids in res_dic.items():
        for return_netid, cnt in return_netids.items():
            fw.write("%s\t%s\t%s\n" % (rent_netid, return_netid, cnt))

    fw.close()

    print "%s has completed!" % csv_name
    
def get_matrixes_of_day(start_time, end_time, net_list, date_time, file_path=None):
    start_time = datetime.datetime.strptime(start_time, '%H%M%S')
    end_time = datetime.datetime.strptime(end_time, '%H%M%S')
    time_delta = datetime.timedelta(minutes = INTERVAL_MINUTES)
    
    now_end   = start_time + time_delta

    while now_end <= end_time:
        start_time_str = start_time.strftime("%H%M%S")
        now_end_str = now_end.strftime("%H%M%S")
        res_dic = create_net_matrix(start_time_str, now_end_str, date_time)
        draw_matrix(res_dic, net_list, date_time+'-'+start_time_str+'-'+str(INTERVAL_MINUTES), file_path)
        
        start_time = now_end
        now_end = start_time + time_delta

    if now_end.strftime("%H") == '00':
        start_time_str = start_time.strftime("%H%M%S")
        last_time_of_day = '235959'
        res_dic = create_net_matrix(start_time_str, now_end_str, date_time)
        draw_matrix(res_dic, net_list, date_time+'-'+start_time_str+'-'+str(INTERVAL_MINUTES), file_path)
        
        

if __name__ == '__main__':
    lis1 = get_netid_list('../derived/rent_netid')
    lis2 = get_netid_list('../derived/return_netid')
    netid_list = sorted(list(set(lis1) | set(lis2)))
    print len(netid_list)
    #f1 = open('net_id.csv','w')
    #f1.write('\n'.join(netid_list))
    #f1.close()
    for date_time in list_date:
        data_path = '../data/day' 
        #print data_path
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        get_matrixes_of_day('070000', '080000', netid_list, date_time, data_path )

    
