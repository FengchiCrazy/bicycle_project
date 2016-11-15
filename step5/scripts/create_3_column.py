import pdb

TRAN_FILE = "../data/xiasha_trans.csv"
STATION_FILE = "../data/stations_xiasha_clustered.csv"
RES_FILE = "res_sep.csv"

station_list = []

with open(STATION_FILE) as data:
    for line_ in data:
        line = line_.strip().split(',')
        station_list.append(line[0])

count_dict = dict([((x, y), 0) for x in station_list for y in station_list])

with open(TRAN_FILE) as data:
    header = data.readline()
    for line_ in data:
        line = line_.strip().split(',')
        rent_netid = line[0]
        return_netid = line[1]

        try:
            count_dict[(rent_netid, return_netid)] += 1
        except:
            pdb.set_trace()

fw = open(RES_FILE, 'w')

res_count = sorted(list(count_dict.items()), key = lambda x: (x[0][0], x[0][1]))

for nets, count in res_count:
    if count > 0:
        fw.write(','.join([nets[0], nets[1], str(count)]) + '\n')

fw.close()



