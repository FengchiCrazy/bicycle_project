library(hflights)
library(dplyr)

class(hflights)
head(hflights)

packageVersion("dplyr")
tbl_hflights <- tbl_df(hflights)
class(tbl_hflights)
tbl_hflights

## select 函数

select(tbl_hflights,Year,Month,DayofMonth,FlightNum,Distance)
select(tbl_hflights,Year:ArrTime)
# 也可以按照倒过来的顺序选择
select(tbl_hflights,ArrTime:Year)
# 除了选择变量，也可以删除指定的变量
select(tbl_hflights,-Year,-Month,-DayofMonth,-FlightNum,-Distance)
select(tbl_hflights,-(Year:ArrTime))

## filter 删选变量

# 选择2011年1月而且起飞时间为1400的所有数据记录
filter(tbl_hflights,Year == 2011, Month == 1, DepTime == 1400)
# '且'的关系也可以用&符号表示，也就是列出的所有条件同时满足
filter(tbl_hflights,Year == 2011 & Month == 1 & DepTime == 1400)
# 选择起飞时间在1400之前的航班
filter(tbl_hflights,Year == 2011 & Month == 1 & DepTime <= 1400)
# '或'的关系用|符号表示。选择起飞时间为1400或者1430的航班,且UniqueCarrier为'AA'
filter(tbl_hflights,Year == 2011 & Month == 1 & (DepTime == 1400 | DepTime == 1430) & UniqueCarrier == 'AA')


## arrange

tbl_hflights1<-select(filter(tbl_hflights,Year == 2011 & Month == 1 & DepTime == 1400),Year:ArrTime,AirTime)
# 将数据按照ArrTime升序排序
arrange(tbl_hflights1,ArrTime)
# 将数据先按照AirTime降序，再按照ArrTime升序排列
arrange(tbl_hflights1,desc(AirTime),ArrTime)

## mutate

# 由ArrTime-DepTime得到航班的飞行所用时长，并存储在DurTime变量中
# 飞行所用时长（单位：分钟）的计算方式为：小时数*60+分钟数
# 同时将飞行的分钟数，换算成秒。
# 优势在于可以在同一语句中对刚增加的列进行操作。
tbl_hflights2<-mutate(tbl_hflights1,
                      DurTime = (as.numeric(substr(ArrTime,1,2)) - as.numeric(substr(DepTime,1,2)))*60 + as.numeric(substr(ArrTime,3,4)) ,
                      Dur_Time1 = DurTime * 60)
tbl_hflights2

## summarize

summarize(tbl_hflights2,avg_dur = mean(DurTime),sum_air = sum(AirTime))[1][1]

### group_by

summarise(group_by(tbl_hflights, UniqueCarrier), 
          m = mean(AirTime,na.rm = TRUE), 
          sd = sd(AirTime,na.rm = TRUE), 
          cnt = n(), 
          me = median(AirTime,na.rm = TRUE))

### %>%
tbl_hflights %>%
  group_by(UniqueCarrier) %>%
  summarize(m = mean(AirTime,na.rm = TRUE), sd = sd(AirTime,na.rm = TRUE)) %>%
  arrange(desc(m),sd) %>%
  head(10)

### sample_n, sample_frac

# 随机抽取10个样本
sample_n(tbl_hflights,10)
# 随机抽取10%的样本
tbl_hflights %>% 
  sample_frac(0.1) %>%
  select(Year:UniqueCarrier) %>%
  group_by(UniqueCarrier) %>%
  summarize(m = mean(ArrTime,na.rm = TRUE), cnt = n()) %>%
  arrange(desc(m))



