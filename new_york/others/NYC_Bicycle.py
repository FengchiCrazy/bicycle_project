# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 19:15:59 2016

@author: fishleongxhh
"""

import os
import numpy as np
from numpy import *
import pandas as pd
from pandas import *
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
#from mpl_toolkits.basemap import Basemap

os.getcwd()
os.chdir('C:\\users\\fishleongxhh\\documents\\Python Scripts\\NYC Bicycle')
os.getcwd()

#读入2014年9月份额度自行车数据
nyc=read_csv('201409-citibike-tripdata.csv',sep=',')
type(nyc)
nyc.ix[1:10,:]
nyc.columns
nyc.dtypes
nyc.columns=['tripduration','start_time','end_time','start_id','start_name','start_lat','start_lon','end_id','end_name','end_lat','end_lon','bike_id','usertype','birth_year','gender']
nyc.columns
nyc.shape
#将站点名剥离出来，单独成一个dataframe
stations_index=nyc.ix[:,['start_id','start_name']].drop_duplicates()
help(nyc.sort_values)
stations_index.sort_values(by='start_id',ascending=True,inplace=True)
stations_index.head()
#删除nyc中的站点名称
help(nyc.drop)
nyc.drop(labels=['start_name','end_name'],axis=1,inplace=True)
nyc.head()
#查看存在缺失值的列
nyc.isnull().any()#只有birth_year存在缺失值

#去除重复值
nyc['usertype'].drop_duplicates()
#Series类型
type(nyc['usertype'])
#分类计数
nyc['usertype'].value_counts()

#站点数目
temp=nyc['start_id'].drop_duplicates()
len(temp)#328个站点
#站点编号的长度计数
temp.map(lambda x:len(str(x))).value_counts()
#大部分站点编号的长度为3，列举出长度为2或4的站点编号
temp[temp.map(lambda x:len(str(x))!=3)]
#将站点id，站点id长度，站点id首位数放进同一个dataframe中
temp=DataFrame({'id':temp,'length':temp.map(lambda x:len(str(x))),'first':temp.map(lambda x:str(x)[0])})
temp.head()
#分类计数
grouped=temp.groupby(by=['length','first'],axis=0)
grouped.count()
#%pylab
fig,ax=plt.subplots(1,1)
grouped.count().plot(kind='bar',ax=ax,xticks=['7_','8-','1--','2--','3--','4--','5--','2---','3---'])
grouped.count().plot(kind='bar')

#查看各变量数据类型
nyc.dtypes
type(nyc.iloc[1,1])
nyc.head()
nyc.iloc[:,[1,2]].tail()
#将起止时间字符串转化为时间类型
nyc['start_time']=nyc['start_time'].map(lambda x:datetime.strptime(x,'%m/%d/%Y %H:%M:%S'))
nyc['end_time']=nyc['end_time'].map(lambda x:datetime.strptime(x,'%m/%d/%Y %H:%M:%S'))
nyc.dtypes
nyc.isnull().any()#只有birth_year存在缺失值

nyc.head()
nyc.iat[1,1]
nyc.iat[1,1].day
nyc.iat[1,1].hour
nyc.iat[10,1].minute
#补充起始月、日、小时、分钟
nyc['start_month']=nyc['start_time'].map(lambda x:x.month)
nyc['start_day']=nyc['start_time'].map(lambda x:x.day)
nyc['start_hour']=nyc['start_time'].map(lambda x:x.hour)
nyc['start_min']=nyc['start_time'].map(lambda x:x.minute)
nyc['end_month']=nyc['end_time'].map(lambda x:x.month)
nyc['end_day']=nyc['end_time'].map(lambda x:x.day)
nyc['end_hour']=nyc['end_time'].map(lambda x:x.hour)
nyc['end_min']=nyc['end_time'].map(lambda x:x.minute)
nyc.head()

#查看9月份每天的借车数
temp=nyc['start_day'].value_counts()
type(temp)#Series类型
temp=temp.sort_index()
temp.plot(kind='bar')
#查看9月份每小时的借车数
temp=nyc['start_hour'].value_counts().sort_index()
temp
temp.plot(kind='bar',colormap='Purples_r')
#查看9月份每小时的还车数
temp=nyc['end_hour'].value_counts().sort_index()
temp
temp.plot(kind='bar',colormap='Purples_r')
#9月份tripduration的分布
nyc['tripduration'].head()/60
#先取对数，再画密度估计图
sns.kdeplot(log(nyc['tripduration']),shade=True)

#查看bikeid的情况
nyc.head()
temp=nyc['bike_id'].drop_duplicates().sort_values()
temp.head()
#bikeid的长度均为5,共5888辆自行车
temp.map(lambda x:len(str(x))).value_counts()
#首位数字是1或2
temp.map(lambda x:str(x)[0]).value_counts()

#查看gender的情况
temp=nyc['gender']
#有0，1，2这三个数字，意义暂时不明
temp.value_counts()

#查看birth_year的情况
temp=nyc['birth_year'].value_counts()
#共有78个年份，意义暂时不明
temp.shape
#最大年份为1998，最小年份为1899
max(temp.index),min(temp.index)

nyc.head()
#各个站点借车操作次数
temp=nyc['start_id'].value_counts()
temp.sort_values(ascending=False,inplace=True)
temp.head()
min(temp),max(temp)
temp.median()
#借车次数的各分位点
percentile(temp,[10,25,50,75,90])
help(sns.kdeplot)
#各站点还车操作次数
temp=nyc['end_id'].value_counts()
temp.sort_values(ascending=False,inplace=True)
temp.head()
min(temp),max(temp)
temp.median()
#还车次数的各分位点
percentile(temp,[10,25,50,75,90])


#7-8点还借车差的情况
nyc.head()
nyc.iat[1,1].hour
nyc['start_time'][1:5].map(lambda x:x.hour>=7 and x.hour<8)
#借车
temp=nyc.ix[nyc['start_time'].map(lambda x:x.hour>=7 and x.hour<8),'start_id'].value_counts()
temp=temp.sort_index()
temp.head()
#还车
temp1=nyc.ix[nyc['end_time'].map(lambda x:x.hour>=7 and x.hour<8),'end_id'].value_counts()
temp1=temp1.sort_index()
temp1.head()
#平均每天的还借车差
temp2=DataFrame({'start':stations_index['start_id'],'end':stations_index['start_id']})
temp2.index=stations_index['start_id']
temp2.ix[temp.index,'start']=temp.values
temp2.ix[temp1.index,'end']=temp1.values
temp2['increase']=(temp2['end']-temp2['start'])/30
temp2.sort_values(by='increase',ascending=True,inplace=True)
#查看有哪些站点借还车差异较大
temp2.head(10)
temp2.tail(10)
#借还车差在5以下、5到10之间、10以上的站点个数
len(temp2.ix[temp2['increase'].map(lambda x:abs(x)<5),'increase'])
len(temp2.ix[temp2['increase'].map(lambda x:abs(x)>=5 and abs(x)<10),'increase'])
len(temp2.ix[temp2['increase'].map(lambda x:abs(x)>=10),'increase'])

#根据还车和借车的差值对站点进行聚类
#分组键
key1=nyc['start_time'].map(lambda x:x.hour)
key2=nyc['end_time'].map(lambda x:x.hour)
#根据站点和分组键进行分组
grouped1=nyc['start_id'].groupby([nyc['start_id'],key1])
grouped2=nyc['end_id'].groupby([nyc['end_id'],key2])
#聚合运算--分组计数，并根据层次化索引转化成dataframe
#index和columbs都已经排好了序
temp1=grouped1.count().unstack()/30
temp1.fillna(0,inplace=True)
temp2=grouped2.count().unstack()/30
temp2.fillna(0,inplace=True)
#temp中存放还车与借车之差
temp=temp2-temp1
temp.iloc[1:5,1:5]
temp.ix[[521,2005],:]
temp.shape
#kmean聚类
kmeans=KMeans(n_clusters=4)
#y_pre中保存各个站点的类别
y_pre=kmeans.fit_predict(temp)
kmeans.n_iter_#迭代次数
#按照类别对站点进行分组
temp.index[1:5]
Series(y_pre).value_counts()
grouped3=temp.index.groupby(y_pre)
type(grouped3)
#查看第0类站点的借还特征
type(grouped3[0])
array(grouped3[0])
temp3=temp.ix[array(grouped3[0]),:]
temp3.T.plot(legend=False)
temp3=temp.ix[array(grouped3[1]),:]
temp3.T.plot(legend=False)
temp3=temp.ix[array(grouped3[2]),:]
temp3.T.plot(legend=False)
temp3=temp.ix[array(grouped3[3]),:]
temp3.T.plot(legend=False)
#对比各类站点的借还特征
#%pylab
fig,axes=plt.subplots(2,2,sharex=True,sharey=True)
for i in range(2):
    for j in range(2):
        temp.ix[array(grouped3[2*i+j]),:].T.plot(xticks=arange(0,24),ax=axes[i,j],legend=False)
fig.show()

import importlib
import mpl_toolkits

importlib.import_module('mpl_toolkits').__path__
