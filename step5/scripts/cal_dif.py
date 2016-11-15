import pdb
SUN_DATA = "xiashaex.csv"
HU_DATA = "../data/stations_xiasha_clustered.csv"

set_hu = set()
set_sun = set()

with open(SUN_DATA) as data:
    line_ = data.readline()
    for line_ in data:
        line = line_.strip().split(',')
        set_sun.add(line[0])
        set_sun.add(line[1])

with open(HU_DATA) as data:
    for line_ in data:
        line = line_.strip().split(',')
        set_hu.add(line[0])

print(set_hu - set_sun)
print(set_sun - set_hu)
pdb.set_trace()
