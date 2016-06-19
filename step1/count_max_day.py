import pdb

car_latest_date = {}
MIN_INTERVAL = 10 
output = {}
ERROR_DATE = ['20130931']

def add_zero(num):
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)

#list_day = ['08', '16', '24', '32']
list_day = [add_zero(x) for x in range(1, 32)]
list_month = ['08', '09', '10', '11']

list_date = ['2013' + m + d for m in list_month for d in list_day]
list_date = [d for d in list_date if d not in ERROR_DATE]

with file('car_date', 'r') as f:
    line = f.readline()
    while line:
        try:
            line = f.readline()
            line = line.strip().split()
            car_num = line[0]
            date = line[1]
            if car_num not in car_latest_date:
                car_latest_date[car_num] = date
            
            idx_date = list_date.index(date)
            idx_old  = list_date.index(car_latest_date[car_num])
            
            if idx_date - idx_old >= MIN_INTERVAL:
                if car_num not in output:
                    output[car_num] = [date]
                else:
                    output[car_num].append(date)
            car_latest_date[car_num] = date
        #pdb.set_trace()
        except:
            line = f.readline()


with file('count_interval_%s_day' % MIN_INTERVAL, 'w') as fw:
    for k, vs in output.items():
        fw.write(k + '\t' + '\t'.join([str(d) for d in vs]) + '\n')
            



