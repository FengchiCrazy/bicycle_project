# -*- coding:utf-8 -*-

import urllib.request, urllib.parse
import datetime

START_DATE = "20130101"
END_DATE   = "20161130" 

def get_date_range():
    start_date_dt = datetime.datetime.strptime(START_DATE, "%Y%m%d")
    end_date_dt   = datetime.datetime.strptime(END_DATE, "%Y%m%d")
    time_delta    = datetime.timedelta(days=1)

    date_range = []
    tmp_dt = start_date_dt
    while tmp_dt <= end_date_dt:
        date_range.append(tmp_dt)
        tmp_dt += time_delta

    return date_range

def get_url(city, datef):
    url = "https://www.wunderground.com/history/airport/"
    if city == 'NY':
        url += 'KNYC/' + datef + "/DailyHistory.html?req_city=New+York&req_state=NY&format=1"
    elif city == "Chicago":
        url += "KMDW/" + datef + "/DailyHistory.html?req_city=Chicago&req_statename=Illinois&format=1"
    elif city == "DC":
        url += "KDCA/" + datef + "/DailyHistory.html?req_city=Washington&req_state=DC&req_statename=District+of+Columbia&format=1"
    
    return url
        

def crawler(city):
    with open("weather_data_%s.csv" % city, 'w') as weather:
        date_range = get_date_range()
        for date in date_range:
            datef = date.strftime("%Y/%m/%d")
            url = get_url(city, datef)

            content = urllib.request.urlopen(url).read()
            content = content.decode()
            contents = content.strip().split('\n')
            date_cont = date.strftime("%Y-%m-%d,")
            for cont in contents[1:]:
                cont = cont.replace('<br />', '')
                weather.write(date_cont + cont + '\n')

            print(date)

if __name__ == '__main__':
    crawler("Chicago")



