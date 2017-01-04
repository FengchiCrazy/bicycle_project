# 胡练
setwd("C:/Users/hulian/Desktop/机器学习/吕晓玲")
data=read.csv("201609-citibike-tripdata.csv",header=T,sep=',')
library(ggplot2)

######usertype
#####条形图
ggplot(data,aes(x=usertype))+geom_bar(width=0.4,fill='lightblue')
#####饼图
usertype.percentage=round(100*prop.table(table(data$usertype)),digits=1)
mylabs=paste(names(usertype.percentage),"\n",usertype.percentage,"%",sep=" ")
pie(usertype.percentage,labels=mylabs,col=c('grey','lightblue'))

#######tripduration
age=2016-data$birth.year
data1=data.frame(data,age)
summary(data1$tripduration)
data1$tripduration[data1$tripduration>2282]=NA
summary(data1$age)
data1$age[data1$age>71.5]=NA
boxplot(data1$tripduration)
data1$gender[data1$gender%in%c('1')]='男'
data1$gender[data1$gender%in%c('2')]='女'
data1$gender[data1$gender%in%c('0')]=NA
data2=subset(data1,select=c(gender,tripduration,age))
ggplot(na.omit(data2),aes(x=gender,y=tripduration))+geom_boxplot()
ggplot(na.omit(data2),aes(x=gender,y=age))+geom_boxplot()
######分性别的usertype
data.male=data1[data1$gender=='男',]
data.female=data1[data1$gender=='女',]
par(mfrow=c(1,2))
usertype.percent1=round(100*prop.table(table(data.male$usertype)),digits=1)
mylabs1=paste(names(usertype.percentage),"\n",usertype.percent1,"%",sep=" ")
pie(usertype.percent1,labels=mylabs1,main="男性",col=c('grey','lightblue'))
usertype.percent2=round(100*prop.table(table(data.female$usertype)),digits=1)
mylabs2=paste(names(usertype.percent2),"\n",usertype.percent2,"%",sep=" ")
pie(usertype.percent2,labels=mylabs2,main="女性",col=c('grey','lightblue'))

#（肖婧学）
data<-read.csv("201609-citibike-tripdata.csv",header=T,sep=",")
bike<-data
library("ggplot2")
##性别比例
bike<-subset(bike,gender!="0")
bike$gender<-ifelse(bike$gender==1,"男","女")
summary(as.factor(bike$gender))
ggplot(bike,aes(x=gender,fill=gender))+geom_bar(width=0.4,fill='lightblue')+
  labs(x="",y="频数")
##年龄构成
bike$age<-2016-bike$birth.year
bike$age1[bike$age<20]<-"20岁以下"
bike$age1[bike$age>=20&bike$age<30]<-"20-30岁"
bike$age1[bike$age>=30&bike$age<40]<-"30-40岁"
bike$age1[bike$age>=40&bike$age<50]<-"40-50岁"
bike$age1[bike$age>=50&bike$age<60]<-"50-60岁"
bike$age1[bike$age>=60&bike$age<70]<-"60-70岁"
bike$age1[bike$age>=70]<-"70岁以上"
bike$age1 = factor(bike$age1, 
                   levels=c('20岁以下','20-30岁','30-40岁','40-50岁','50-60岁','60-70岁','70岁以上')) 
summary(bike$age1)
bike<-subset(bike,age1!="NA")
ggplot(bike,aes(x=age1))+geom_bar(width=0.4,fill='lightblue')+
  labs(x="",y="频数")
##时刻
bike$starttime[bike$starttime<=5]<-"5点及以前"
bike$starttime=factor(bike$starttime,
                      level=c("5点及以前","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"))
summary(bike$starttime)
ggplot(bike,aes(x=starttime))+geom_bar(width=0.5,fill='lightblue')+
  labs(x="出发时间",y="频数")
##星期
bike$date<-as.Date(bike$date,"%m/%d/%Y")
bike$week<-format(bike$date,format("%A"))
bike$week<-factor(bike$week,
                  levels=c('星期一','星期二','星期三','星期四','星期五','星期六','星期日'))
bike1<-subset(bike,bike$date<as.Date("2016-09-15"))
summary(bike1$week)
ggplot(bike1,aes(x=week,fill=factor(week)))+geom_bar(width=0.4)+
  labs(x="",y="频数")+
  theme(legend.position="none")
##时长
bike<-subset(bike,tripduration<=4000)
summary(bike$tripduration)
binsize<-diff(range(bike$tripduration))/30
ggplot(bike,aes(x=tripduration))+
  geom_histogram(aes(y=..density..),binwidth=binsize,fill="pink",colour="blue")+
  labs(x="时长(单位：秒)",y="概率密度")
