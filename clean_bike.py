import datetime
import pandas as pd
import numpy as np

# parameter 
FILE_NAME = "data_bike.csv"
START_DATE = "20130813"
END_DATE   = "20131113" 

bike_num_dict = {
    '5022': 1,
    '5064': 2,
    '5065': 3,
    '5066': 4,
    '5071': 5,
    '5147': 6,
    '5149': 7,
    '5158': 8,
    '5160': 9,
    '5161': 10,
    '5162': 11,
    '5163': 12,
    '5166': 13,
    '5168': 14,
    '5169': 15,
    '5170': 16,
    '5175': 17,
    '5198': 18,
    '5199': 19,
    '5200': 20,
    '5201': 21,
    '5202': 22,
    '5203': 23,
    '5204': 24,
    '5211': 25,
    '5291': 26,
    '5370': 27,
    '5371': 28,
    '5399': 29,
    '5400': 30,
    '5412': 31,
    '5421': 32,
    '5422': 33,
    '5492': 34,
    '5509': 35,
    '8003': 36,
    '8004': 37,
    '8017': 38,
    '8033': 39
}

hour_range = [str(x) for x in range(5, 22)]

# date range
start_time = datetime.datetime.strptime(START_DATE, "%Y%m%d")
end_time   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
time_delta = datetime.timedelta(days=1)

date_range = []
while start_time <= end_time:
    date_range.append(start_time)
    start_time += time_delta

# row keys and column keys
row_key = [x.strftime("%m%d") + '-' + y for x in date_range for y in hour_range]
column_key = [str(x) + '-' + str(y) for x in range(1, 40) for y in range(1, 40)]

# create a zero dataframe
zero_matrix = np.zeros((len(row_key), len(column_key)), dtype = np.int)
df = pd.DataFrame(zero_matrix, index = row_key, columns = column_key)
row_key_set = set(row_key)


with open(FILE_NAME, 'r') as data:
    # handle header
    line_ = data.readline()
    while True:
        line_ = data.readline()
        line  = line_.strip().split(',')
        if len(line) <= 1:
            break
            
        rent_netid = bike_num_dict[line[0]]
        return_netid = bike_num_dict[line[1]]
        net_key = str(rent_netid) + '-' + str(return_netid)
        time_key = line[2][4:] + '-' + line[7]
        if time_key in row_key_set:
            df.loc[time_key, net_key] += 1

#save result
df.to_csv("result.csv")
