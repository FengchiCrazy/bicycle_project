library(readr)
bike = read_csv("../../ny/201609-citibike-tripdata.csv")
bike$starttime = as.POSIXct(bike$starttime,format="%m/%d/%Y %H:%M:%S")
print(paste("自行车数:",length(unique(bike$bikeid)),sep=""))
print(paste("站点数:",length(unique(bike$`start station id`)),sep=""))

# 分时间段考虑借车次数，以starttime为准
# 存在两段波峰
bike$hid = format(bike$starttime,"%H")
a=paste(00:23,"00",sep = ":")
b=paste(01:24,"00",sep = ":")
cc=table(bike$hid)
names(cc)=paste(a,b,sep="-")
# par(las = 3,cex.axis=.8)
barplot(cc,col = "lightblue")

# 频繁站点分析：以start station为准
# 纵坐标可以理解为操作次数
stid = table(bike$`start station id`)
sstid = stid[order(stid,decreasing = T)]
s = c(seq(0,7000,by = 200),
      seq(8000,17000,by=1000))
# 0-7000次按200为间隔,
# 8000-17000按1000为间隔
sstid = cut(sstid,breaks = s)
sstid = table(sstid)
opar = par(no.readonly = T)
par(mar = c(5,7,4,2),las = 1,cex.axis=.8)
barplot(sstid,xlab = "车站数",col = "lightblue",horiz = T)
par(opar)
# 频繁站点分析：以end station为准
etid = table(bike$`end station id`)
eetid = etid[order(etid,decreasing = T)]
eetid = cut(eetid,breaks = s)
eetid = table(eetid)
opar = par(no.readonly = T)
par(mar = c(5,7,4,2),las = 1,cex.axis=.8)
barplot(eetid,xlab = "车站数",col = "lightblue",horiz = T)
par(opar)

# 9月发生借还次数做多的车站为同一个
# 输出借、还次数 经纬度 name
names(which.max(stid))
names(which.max(etid))
stid[which.max(stid)]
etid[which.max(stid)]
c(bike$`start station latitude`[bike$`start station id`==519][1],
  bike$`start station longitude`[bike$`start station id`==519][1])
bike$`start station name`[bike$`start station id`==519][1]


# 频繁车辆分析
# 纵坐标为使用次数
bid = table(bike$bikeid)
bbid = bid[order(bid,decreasing = T)]
min(bbid)
max(bbid)
s = seq(10,420,by = 10)
bbid = cut(bbid,breaks = c(0,5,s))
bbid = table(bbid)
opar = par(no.readonly = T)
par(mar = c(5,4,4,2),las = 1,cex.axis=.8)
# 不同使用次数区间车辆数
barplot(bbid,xlab = "车辆数",col = "lightblue",horiz = T)
par(opar)

sum(bid<5)
# 61辆车9月使用次数小于5次
N = names(bid[bid<5])
B = bike[bike$bikeid%in%N,]
# 16722号自行车
bi = bike[bike$bikeid == "16722",]
bi$did = format(bi$starttime,"%d")
plot(bi$did,bi$tripduration)


# 定义一次损坏：起始站和结束站一致，时间小于1分半钟
may = bike[bike$tripduration<90,]
may2 = may[may$`start station id`==may$`end station id`,]
tt=table(may2$bikeid)
table(tt)

# 损坏识别
# 出现疑似损坏次数为3的单车
names(tt[tt==3])
bike3 = bike[bike$bikeid == "25084",]
bike3$did = format(bike3$starttime,"%d")
plot(bike3$did,bike3$tripduration)

# 出现疑似损坏次数为4的单车
names(tt[tt==4])
bike4 = bike[bike$bikeid == "14680",]
bike4$did = format(bike4$starttime,"%d")
plot(bike4$did,bike4$tripduration)

# 出现疑似损坏次数为5的单车
names(tt[tt==5])
bike5 = bike[bike$bikeid == "22222",]
bike5$did = format(bike5$starttime,"%d")
plot(bike5$did,bike5$tripduration)


# 出现疑似损坏次数为6的单车
names(tt[tt==6])
bike6 = bike[bike$bikeid == "22449",]
bike6$did = format(bike6$starttime,"%d")
plot(bike6$did,bike6$tripduration)

# 出现疑似损坏次数为11的单车
names(tt[tt==11])
bike11 = bike[bike$bikeid == "23759",]
bike11$did = format(bike11$starttime,"%d")
plot(bike11$did,bike11$tripduration, xlab = "date", ylab = "trip duration", main = "23759 bike use time")

