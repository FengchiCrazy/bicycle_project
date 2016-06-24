library(ggplot2)
library(ggmap)

setwd("C:\\Users\\Administrator\\Desktop\\drawing")
data_list <- dir()
#data_list <- c('1006.csv')
xlim_left <- strptime("06:00:00", "%H:%M:%S")
xlim_right <- strptime("22:00:00", "%H:%M:%S")
for (i in 1: 20){
csv_data <- read.csv(data_list[i])
name = as.character(strsplit(data_list[i], '.csv'))
csv_data$time1 <- strptime(csv_data$time, format = "%H:%M:%S")

# 借车时间
ggplot(csv_data) +
    geom_density(aes(time1, color=date), alpha = 0.1, show.legend=FALSE) +
    geom_density(aes(time1), weight = 5, size = 2) +
    xlim(xlim_left, xlim_right) +
    ylim(0, 12e-05) +
    labs(title = paste("rent_time", name, sep = " "))
ggsave(file = paste("../rent_time/", name, '.png', sep = ""))

# 借车gap时间折线图
# 这部分图像不清楚后来被老师取消了
#ggplot(csv_data) +
#   geom_line(aes(time1, gap, color = date), alpha=0.5, show.legend=FALSE) +
#   xlim(xlim_left, xlim_right) +
#   ylim(0, 3600)

#csv_data$hour <- as.factor(csv_data$hour)

#  box plot
ggplot(csv_data) +
    geom_boxplot(aes(hour, gap)) +
    ylim(0, 5500) +
    labs(title = paste("boxplot", name, sep = " "))
ggsave(file = paste("../boxplot/", name, '.png', sep = ""))

ggplot(csv_data) +
    geom_boxplot(aes(hour, log2(gap))) +
    ylim(0, 20) +
    labs(title = paste("boxplot_log2", name, sep = " "))
ggsave(file = paste("../boxplot_log/", name, '.png', sep = ""))
}


# to do: 画地图，各站点热力图
hz_map <- get_map(location = "hangzhou", zoom = 13, maptype = 'roadmap', crop = TRUE)
# 读各站点经纬度数据
nd <- read.csv("less_20.csv")

# 读入gap时间数据
gap_day <- read.csv('gap.csv')
gap_day <- gap_day[,c("net_id", "hour")]
gap_day <- na.omit(gap_day)
gap_day <- merge(gap_day, nd, all.x = TRUE)
gap_day <- na.omit(gap_day)

for (i in 6: 21){
    #i <- 7
    gap_i <- gap_day[gap_day$hour == i,]
    ggmap(hz_map) +
        stat_density_2d(data = gap_i,aes(x=lon,y=lat, fill = ..level..), geom = "polygon", alpha = 0.7) +
        scale_fill_gradient(low = "grey", high = "red") +
        labs(title = paste("median gap in hour", i, sep = " "))
    ggsave( file = paste("gap_",i,".png", sep=""))
}

# 读入count时间数据
count_day <- read.csv('count.csv')
count_day <- count_day[,c("net_id", "hour")]
count_day <- merge(count_day, nd, all.x = TRUE)
count_day <- na.omit(count_day)

for (i in 6:21) {
    count_i <- count_day[count_day$hour == i, ]
    
    ggmap(hz_map) +
        stat_density_2d(data = count_i,aes(x=lon,y=lat, fill = ..level..), geom = "polygon", alpha = 0.7) +
        scale_fill_gradient(low = "grey", high = "red") +
        labs(title = paste("median count in hour", i, sep = " "))
    ggsave(file = paste("count_", i, ".png" ,sep=""))
    
}