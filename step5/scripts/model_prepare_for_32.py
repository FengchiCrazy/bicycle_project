import datetime
from collections import defaultdict
import pdb

FILE_NAME = "../data/xiasha_trans.csv"
START_DATE = '20130902'
END_DATE   = '20130929'

hour_range = range(0, 24)

# date range
start_time = datetime.datetime.strptime(START_DATE, "%Y%m%d")
end_time   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
time_delta = datetime.timedelta(days=1)

date_range = []
while start_time <= end_time:
    date_range.append(start_time)
    start_time += time_delta

keys = [d.strftime('%m%d') + '_' + str(h) for h in hour_range for d in date_range]

count_dict = dict([(key, 0) for key in keys])

with open(FILE_NAME, 'r') as data:
    line_ = data.readline()
    while True:
        line_ = data.readline()
        line  = line_.strip().split(",")
        if len(line) <= 1:
            break
        
        date = line[2][4:]
        hour = str(int(line[3][:2]))
     
        key = date + '_' + hour
        count_dict[key] += 1
        
    
read_file_name = "../data/weather_output.csv"
target_file_name = "../data/model_32.csv"

fw = open(target_file_name, 'w')

with open(read_file_name, 'r') as data:
    line_ = data.readline()
    fw.write("date,weekday,hour,temp,sunny,windy,count\n")
    
    while True:
        line_ = data.readline()
        line  = line_.strip().split(',')
        if len(line) <= 1:
            break
        
        key = line[0]

        if key not in count_dict:
            count = 0
        else:
            count = count_dict[key]
        
        date = '2013' + line[0].split("_")[0]
        weekday = datetime.datetime.strptime(date, '%Y%m%d').strftime("%w")
        hour = line[0].split("_")[1]
        temp = line[1]
        sunny = line[2]
        windy = line[3]
        
        out_list = [date, str(weekday), hour, temp, sunny, windy, str(count)]
            
        
        fw.write(','.join(out_list) + '\n')

fw.close()


