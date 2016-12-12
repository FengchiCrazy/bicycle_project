from urllib.request import urlopen
from xml.etree.ElementTree import parse
from lxml import etree
import pdb

#xml = urlopen("https://feeds.capitalbikeshare.com/stations/stations.xml").read()
#root = etree.El
#xml = eval(open("station.xml").read())
#print(xml)

#pdb.set_trace()
tree = None
try:
    tree = parse("station.xml")
except Exception as e:
    print(str(e)[:100])
    print(type(e))
    print(e.args)
if tree:
    print("HAHA")
else:
    print("Oh NO")

station = open("station_data_1.csv", "w")
attribute_list = ["id", "name", "lat", "long", "nbBikes", "nbEmptyDocks", "installed", "locked", "temporary", "public"]
station.write(','.join(attribute_list) + '\n')

for item in tree.iterfind("station"):
    #id_   = item.findtext("id")
    #name  = item.findtext("name").replace("&amp;", "&")
    #lat   = item.findtext("lat")
    #long_ = item.findtext("long")
    #nbBikes = item.findtext("nbBikes")
    #nbEmptyDocks = item.findtext("nbEmptyDocks")
    #installed = item.findtext("installed")
    #locked = item.findtext("locked")
    #temporary = item.findtext("temporary")
    #public = item.findtext("public")

    #print(id_)
    #print(name)
    #print(lat)
    #print(long_)
    #print(nbBikes)
    #print(nbEmptyDocks)
    #print(installed)
    #print(locked)
    #print(temporary)
    #print(public)
    #print()
    #station.write(",".join([id_, name, lat, long_, nbBikes, nbEmptyDocks, installed, locked, temporary, public]) + '\n')
    n = len(attribute_list)
    for ix, attr in enumerate(attribute_list):
        station.write(item.findtext(attr))
        if ix < n - 1:
            station.write(',')
        else:
            station.write('\n')

