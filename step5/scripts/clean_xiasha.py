import os
import sys
import pdb

DATA_FOLDER = "/home/dmc/project/bike/"
XIA_SHA_STATION = "../data/stations_xiasha_clustered.csv"

xiasha_set = set()

with open(XIA_SHA_STATION) as data:
    for line_ in data:
        line = line_.strip().split(',')
        station_id = line[0]
        xiasha_set.add(station_id)

data_list = [x for x in sorted(os.listdir(DATA_FOLDER)) if x[:5] == 'trans']

#pdb.set_trace()
xiasha_trans_file = "../data/xiasha_trans.csv"

fw = open(xiasha_trans_file, 'w')
# header
fw.write(','.join([
                "rent_netid",
                "return_netid",
                "tran_date",  
                "tran_time",
                "return_date",
                "return_time",
                "car_num",
            ])+ '\n')
    

for data_file in data_list:
    with open(DATA_FOLDER + data_file) as data:
        header = data.readline()
        for line_ in data:
            line = line_.strip().split(',')
            rent_netid = line[1]
            tran_date  = line[2]
            tran_time  = line[3]
            car_num    = line[6]
            return_netid = line[8]
            return_date  = line[11]
            return_time  = line[12]
            tran_flag    = line[13]

            if rent_netid in xiasha_set and return_netid in xiasha_set \
                and tran_date >= '20130902' and tran_date <= '20130929' and \
                tran_flag in set(['1', '2']):
                out_list = [
                    rent_netid, 
                    return_netid,
                    tran_date,  
                    tran_time,
                    return_date,
                    return_time,
                    car_num,
                ]
                fw.write(','.join(out_list) + '\n')

fw.close()
