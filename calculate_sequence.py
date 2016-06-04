import pdb
time_list = []

def add_zero(num):
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)

#list_day = ['08', '16', '24', '32']
list_day = [add_zero(x) for x in range(1, 32)]
list_month = ['08', '09', '10', '11']

# the minimum of the total count
# if you want all cars result, the value should be set 0
MIN_COUNT = 300 

for m in list_month:
    for d in list_day:
        time_list.append('2013-' + m + '-' + d)

time_list = time_list[:-2]

fw = open('count_everyday', 'w')
fw.write('car_num\ttotal_count\t')
fw.write('\t'.join(time_list))
fw.write('\n')

with open('result_2min', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip().split()
        car_num = line[0]
        total_count = line[1]
        if int(total_count) < MIN_COUNT:
            line = f.readline()
            continue
        acc_list = sorted(line[2:])
        now = 0
        j = 0
        res = [0 for x in time_list]
        for i in range(len(acc_list)):
            while acc_list[i] > time_list[j]:
                j += 1
            res[j] += 1
        
        fw.write("%s\t%s\t" % (car_num, total_count))
        fw.write("\t".join([str(x) for x in res]))
        fw.write("\n")

        line = f.readline()

fw.close()


