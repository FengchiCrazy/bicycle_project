#-*- coding:utf-8 -*-
import datetime
import pdb

FILE_NAME = "weather.csv"
MIN_TEMP_HOUR = 5
MAX_TEMP_HOUR = 14
DAY_HOURS     = 24

START_DATE = "2013-08-01"
END_DATE   = "2013-11-14"

hour_range = range(5, 22)

def get_temp(hour, min_temp, max_temp, last_max_temp=None, next_min_temp=None):
    if hour == MIN_TEMP_HOUR:
        return min_temp
    elif hour == MAX_TEMP_HOUR:
        return max_temp
    elif hour > MIN_TEMP_HOUR and hour < MAX_TEMP_HOUR:
        return float(max_temp - min_temp) / (MAX_TEMP_HOUR - MIN_TEMP_HOUR) * (hour - MIN_TEMP_HOUR) + min_temp
    elif hour < MIN_TEMP_HOUR:
        return float(last_max_temp - min_temp) / (MIN_TEMP_HOUR + DAY_HOURS - MAX_TEMP_HOUR) * (MIN_TEMP_HOUR - hour) + min_temp
    elif hour > MAX_TEMP_HOUR:
        return float(max_temp - next_min_temp) / (MIN_TEMP_HOUR + DAY_HOURS - MAX_TEMP_HOUR) * (hour - MAX_TEMP_HOUR) + next_min_temp

def sunny_or_not(hour, weather_string):
    if "转" in weather_string:
        weather_ = weather_string.split("转")
        if hour <= MAX_TEMP_HOUR:
            weather = weather_[0]
        else:
            weather = weather_[1]
    else:
        weather = weather_string
    
    
    if "雨" in weather:
        return False
    else:
        return True

def windy_or_not(wind_string):
    if "3" in wind_string:
        return False
    else:
        return True

def dummy_changer(value):
    if value:
        return '1'
    else:
        return '0'

class LineContainer(object):
    def __init__(self, date, max_temp, min_temp, weather_string, wind_string):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.weather_string = weather_string
        self.wind_string = wind_string

class TempContainer(object):
    def __init(self, last_max_temp, min_temp, max_temp, next_min_temp):
        self.last_max_temp = last_max_temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.next_min_temp = next_min_temp

start_date = datetime.datetime.strptime(START_DATE, "%Y-%m-%d")
end_date   = datetime.datetime.strptime(END_DATE, "%Y-%m-%d")

fw = open("weather_output.csv", "w")
fw.write("date_hour,temp,sunny,windy\n")

with open(FILE_NAME, "r") as data:
    line_ = data.readline()
    while True:
        line_ = data.readline()
        line = line_.strip().split(' , ')
        if len(line) <= 1:
            break
        
        date           = datetime.datetime.strptime(line[0], "%Y-%m-%d")
        max_temp       = int(line[1])
        min_temp       = int(line[2])
        weather_string = line[3]
        wind_string    = line[5]

        this_line = LineContainer(date, max_temp, min_temp, weather_string, wind_string)
        
        if date < start_date or date > end_date:
            last_line = this_line
            continue
        
        else:
            for hour in hour_range:
                temp = get_temp(hour, last_line.min_temp, last_line.max_temp, next_min_temp = this_line.min_temp)
                sunny = sunny_or_not(hour, last_line.weather_string)
                wind  = windy_or_not(last_line.wind_string)
                fw.write(last_line.date.strftime("%m%d_") + \
                        str(hour) + ',' + str(round(temp, 2)) + ','\
                        + dummy_changer(sunny) + ',' + dummy_changer(wind) + '\n')

            last_line = this_line

fw.close()

        
