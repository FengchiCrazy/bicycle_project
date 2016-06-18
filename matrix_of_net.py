from time_handle_tools import time_handle, list_date
import pdb
import os
import pandas as pd
import numpy as np
import datetime
from ConfigParser import ConfigParser

INTERVAL_MINUTES = 60
# the derived file from hive
# **the first columns of file must be tran_time, rent_netid, return_netid, tran_date**
PARSE_FILE_NAME = netid_7_to_8
PARSE_FILE = "%s%sderived%s%s" % (os.path.pardir, os.sep, os.sep, PARSE_FILE_NAME)
            
def draw_matrix(res_dic, net_list, csv_name, file_path=None):
    df = pd.DataFrame(index=net_list, columns=net_list)
    for rent_netid, return_netids in res_dic.items():
        for return_netid, cnt in return_netids.items():
            df[rent_netid][return_netid] = cnt

    if file_path:
        df.to_csv('%s%s%s' % (file_path, os.sep, csv_name))
    else:
        df.to_csv(csv_name)
    
def get_matrixes_of_day(start_time, end_time, net_list, date_time, file_path=None):
    start_time = datetime.datetime.strptime(start_time, '%H%M%S')
    end_time = datetime.datetime.strptime(end_time, '%H%M%S')
    time_delta = datetime.timedelta(minutes = INTERVAL_MINUTES)
    
    now_end   = start_time + time_delta

    while now_end <= end_time:
        start_time_str = start_time.strftime("%H%M%S")
        now_end_str = now_end.strftime("%H%M%S")
        res_dic = create_net_matrix(start_time_str, now_end_str, date_time)
        draw_matrix(res_dic, net_list, date_time+'-'+start_time_str, file_path)
        return res
                
def draw_matrix(res_dic, net_list, csv_name, file_path=None):
    #zero_arr = np.zeros((len(net_list),len(net_list)), dtype=np.int)
    df = pd.DataFrame(index=net_list, columns=net_list)
    for rent_netid, return_netids in res_dic.items():
        for return_netid, cnt in return_netids.items():
            df[rent_netid][return_netid] = cnt

    if file_path:
        df.to_csv('%s%s%s.csv' % (file_path, os.sep, csv_name))
    else:
        df.to_csv('%s.csv' % csv_name)

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
        draw_matrix(res_dic, net_list, date_time+'-'+start_time_str+'-'+INTERVAL_MINUTES, file_path)
        
        start_time = now_end
        now_end = start_time + time_delta
            

if __name__ == '__main__':
    lis1 = get_netid_list('../derived/rent_netid')
    lis2 = get_netid_list('../derived/return_netid')
    netid_list = list(set(lis1) | set(lis2))
    print len(netid_list)
    for date_time in ['20130913', '20130914']:
        get_matrixes_of_day('070000', '080000', netid_list, date_time)

    
