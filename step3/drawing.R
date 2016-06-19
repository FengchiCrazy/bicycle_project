nd <- read.csv('net_id_ll.csv')
nd <- nd[nd$net_id != 3746,]
nd <- nd[nd$net_id != 3487,]

library(ggplot2)
library(ggmap)

#example
#df <- structure(list(Station.Area = c("Balbriggan", "Blanchardstown", "Dolphins Barn", "Donnybrook", "Dun Laoghaire", "Finglas"), 
#										 Latitude = c(53.608319, 53.386813, 53.333532, 53.319259, 53.294396, 53.390325), 
#										 Longitude = c(-6.18208, -6.377197, -6.29146, -6.232017, -6.133867, -6.298401)), 
#								     .Names =c("Station.Area","Latitude", "Longitude"), 
#										 row.names = c(NA, 6L), class = "data.frame")
#dub_map <- get_map(location = "Dublin", zoom = "auto", scale="auto", crop = TRUE, maptype = "hybrid")
#
#ggmap(dub_map) +
#geom_point(data = df, aes(x = Longitude, y = Latitude))

name = '6117'
csv_name <- paste(name,'.csv', sep = "")
csv_data <- read.csv(csv_name)

csv_data$time1 <- strptime(csv_data$time, format = "%H:%M:%S")

xlim_left <- strptime("06:00:00", "%H:%M:%S")
xlim_right <- strptime("22:00:00", "%H:%M:%S")

# 借车时间
ggplot(csv_data) +
	geom_density(aes(time1, color=date), alpha = 0.1, show.legend=FALSE) +
	geom_density(aes(time1), weight = 5, size = 2) +
	xlim(xlim_left, xlim_right) +
	ylim(0, 7.5e-05)

csv_data$date1 <- as.Date(csv_data$date)
csv_data$date1

ggplot(csv_data) +
	geom_line(aes(time1, gap, color = date), alpha=0.5, show.legend=FALSE) +
	xlim(xlim_left, xlim_right) +
	ylim(0, 3600)

nr <- nrow(csv_data)
for (i in 1:nr) {
	hour = unclass(csv_data[i,]$time1)$hour
	csv_data[i,]$hour = hour
}

csv_data$hour <- as.factor(csv_data$hour)


# box plot
ggplot(csv_data) +
	geom_boxplot(aes(hour, gap)) +
	ylim(0, 1500)	

ggplot(csv_data) +
	geom_boxplot(aes(hour, log2(gap))) +
	ylim(0, 15)



hz_map <- get_map(location = "hangzhou", zoom = 13, maptype = 'roadmap', crop = TRUE)
ggmap(hz_map) +
	geom_point(data = nd, aes(x = lon, y = lat))

p <- ggmap(get_googlemap(center='hangzhou', zoom=13, maptype = 'roadmap'), extent = 'device')
p + geom_point(data = nd[nd$is_24 == 1, ], aes(x=lon,y=lat), color='red', size = 3, alpha = 0.7) +
	geom_point(data = nd[nd$is_24 ==0, ], aes(x=lon,y=lat), color='blue', size = 2, alpha = 0.4)


gap_day <- read.csv('gap.csv')
gap_day <- merge(gap_day, nd, all.x = TRUE)
class(gap_day$hour)
head(gap_day_new)

for (i in 6: 21){
	# pic_gap <- paste("gap_",i,".jpg", sep = "")
	# jpeg(file = pic_gap)
	i <- 7
	gap_i <- gap_day[gap_day$hour == i,]
	#hz_map <- get_map(location = "hangzhou", zoom = 13, maptype = 'roadmap', crop = TRUE)
	ggmap(hz_map) +
		geom_point(data = gap_i[gap_i$is_24 == 1, ], aes(x=lon,y=lat, size = median_gap, color=median_gap)) +
		geom_point(data = gap_i[gap_i$is_24 ==0, ], aes(x=lon,y=lat, size = median_gap, color=median_gap)) +
		scale_colour_gradient(low = "white", high = "red")
	# dev.off()
}
