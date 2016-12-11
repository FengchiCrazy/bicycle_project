# -*- coding:utf-8 -*-

import urllib.request, urllib.parse
import datetime

START_DATE = "20100101"
END_DATE   = "20161130" 

start_date_dt = datetime.datetime.strptime(START_DATE, "%Y%m%d")
end_date_dt   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
time_delta    = datetime.timedelta(days=1)

date_range = []
tmp_dt = start_date_dt
while tmp_dt <= end_date_dt:
    date_range.append(tmp_dt)
    tmp_dt += time_delta


with open("weather_data.csv", 'w') as weather:
    for date in date_range[:1]:
    

        URL = "https://www.wunderground.com/history/airport/KNYC/" + \
                date.strftime("%Y/%m/%d") + \
                "/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=&reqdb.zip=10001&reqdb.magic=10&reqdb.wmo=99999&format=1"

        content = urllib.request.urlopen(URL).read()
        content = content.decode()
        contents = content.strip().split('\n')
        date_cont = date.strftime("%Y-%m-%d,")
        for cont in contents[1:]:
            cont = cont.replace('<br />', '')
            weather.write(date_cont + cont + '\n')
            
        #weather.write(content + '\n')

        print(date)




