# -*- coding:utf-8 -*-
"""
使用方法：
1.首先从hive中上下架表中导出数据，数据前三列分别是借车站点，借车日期，借车时间 或者 还车站点，还车日期，换车时间
    eq: select car_num, tran_date, tran_time from tran where tran_date = 20130901 and tran_time >= 60000 and tran_time <= 220000;
2.设置变量data_file值为刚才导出的文件
3.设置变量out_put_file_name为输出的excel文件的名字，不用加后缀名
4.设置target_list值为需要研究的站点，list中每一个值为字符串


输出文件格式为：
out_put_file_name.xls文件中，target_list中的每一个站点为一个sheet，每一个sheet中只有一列值，
为从早到晚的时间数据，格式为%H:%M:%S

注：
1.借还站点不能一次生成，要两次运行程序，设置不同的导出文件以及输出文件名
2.*****要注意每输出一次文件要更改一次输出文件名，否则新生成的文件会覆盖原有文件****
"""

from collections import defaultdict
import xlwt
import datetime
import pdb

data_file = 'return_netid_time'
out_put_file_name = 'return_20130901'

target_list = ['6117', '6001', '6205', '6211', '6115',
               '6005', '6090', '6116', '6152', '6026']

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

for line in fd:
    data = line.strip().split()
    net_id = data[0]
    date = data[1]
    time = time_handle(data[2])
    if time is None:
        continue

    res[net_id].append(date + time)

fd.close()
    
out_put = xlwt.Workbook()
for net_id in target_list:
    # print res[net_id]
    table = out_put.add_sheet(net_id)
    # pdb.set_trace()
    lis_time = res[net_id]
    lis_time.sort()
    for i in range(len(lis_time)):
        date_time = datetime.datetime.strptime(lis_time[i], "%Y%m%d%H%M%S").strftime("%H:%M:%S")
        table.write(i, 0, date_time)

out_put.save('%s.xls' % out_put_file_name)
