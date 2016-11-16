import datetime
import pdb
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kstest, describe
from collections import defaultdict


# DATA_DIR = os.pardir + os.sep + 'data' + os.sep
DATA_DIR = ""
TRAN_FILE = "xiasha_trans.csv"
CLUSTER_FILE = "stations_xiasha_clustered.csv"
IMG_FOLDER = os.getcwd() + os.sep + 'img' + os.sep

MIN_P = 0.05 
CLUSTER_NUM = 10

RES_MATRIX_NAME = "matrix_35.csv"

def my_round(number, digits = 5):
    return round(number, 5)

def my_out(string, file_obj = None):
    if file_obj:
        file_obj.write(string + '\n')
    else:
        print(string)

cluster_dict = {}
cluster_tran = defaultdict(list)

with open(DATA_DIR + CLUSTER_FILE) as data:
    for line_ in data:
        line = line_.strip().split(',')
        netid = line[0]
        clusterid = line[4]

        cluster_dict[netid] = clusterid

with open(DATA_DIR + TRAN_FILE) as data:
    header = data.readline()
    for line_ in data:
        line = line_.strip().split(',')

        rent_netid   = line[0]
        return_netid = line[1]
        rent_date    = line[2]
        rent_time    = line[3]
        return_date  = line[4]
        return_time  = line[5]

        try:
            rent_dt = datetime.datetime.strptime(rent_date + rent_time, "%Y%m%d%H%M%S")
            return_dt = datetime.datetime.strptime(return_date + return_time, "%Y%m%d%H%M%S")
        except:
            pdb.set_trace()
        if rent_dt > return_dt:
            print(line_.strip())
            continue
        else:
            interval = (return_dt - rent_dt).seconds

        cluster_tran[(cluster_dict[rent_netid], cluster_dict[return_netid])].append(interval)

res_cluster = sorted(cluster_tran.items(), key = lambda x: (x[0][0], x[0][1]))
print(res_cluster[0])

cluster_index = [str(i) for i in range(CLUSTER_NUM)]
res_df = pd.DataFrame(None, index = cluster_index, columns = cluster_index)


def draw_log_hist(clusters, log_seconds, p_val):
    n2, bins2, patches2 = plt.hist(log_seconds, bins = 10)
    plt.xlabel("Log seconds")
    plt.ylabel("count")
    title = "hist of seconds between C" + clusters[0] + " and C" + clusters[1] + '  KS p_value=' + str(p_val)
    print(title)
    plt.title(title)
    plt.savefig(IMG_FOLDER + clusters[0] + '_' + clusters[1] + '.png', format = 'png')
    plt.clf()

# log normal distribution test && param estimated
for clusters, seconds in res_cluster:
    n = len(seconds)
    # n1, bins1, patches1 = plt.hist(seconds, bins = 10)
    # pdb.set_trace()
    log_seconds = np.log(seconds)
    p_val = my_round(kstest(log_seconds, 'norm')[1])

    draw_log_hist(clusters, log_seconds, p_val)
    print(str(clusters) + ':')
    print(str(describe(log_seconds)) + '\n')
    if p_val <= MIN_P:
        print(str(clusters) + '  KS p_value=' + str(p_val))
    else:
        miu_hat = my_round(np.sum(log_seconds) / n)
        sigma_hat = my_round(np.sum(np.pow(log_seconds - miu_hat, 2)) / n)

        res_df.loc[clusters[0], clusters[1]] = '(' + str(miu_hat) + ',' + str(sigma_hat) +')'


res_df.to_csv(RES_MATRIX_NAME, sep = "|")
