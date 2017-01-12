#! /usr/local/bin/Rscript

setwd("/Users/ErnestWu/Desktop/Ny_bike")
library(data.table)

res_cluster1 <- fread("cluster1.csv", header = TRUE)
res_cluster1 <- subset(res_cluster1, select = c(-1))
colnames(res_cluster1) <- c('statID', 'lat', 'lon', 'cluster')

res_cluster_loc <- fread("cluster2.csv", header = TRUE)
colnames(res_cluster_loc) <- c('statID', 'lat', 'lon', 'cluster')

library(ggplot2)
library(ggmap)

#geocode('NewYork')
#ggplot(aes(x=, y=lat), data=res_cluster1) +
#  geom_blank() + coord_map("cluster") +
#  annotation_raster(ggmap,xmin, xmax, ymin, ymax)

#airmap<-qmap(center = c(-74.01658,40.71534),zoom=12,extent="device",legend="none")
#airmap + geom_point(data = res_cluster1, aes(x=lon, y=lat,colour=cluster))

my_map <- get_map(location = c(-73.96324, 40.73324),zoom=12)
cluster_map_1 <- ggmap(my_map) + 
                       geom_point(data = res_cluster1, aes(x=lon, y=lat,colour=factor(cluster)),size=3) +
                       theme(text = element_text(family = 'STKaiti')) +
                       labs(x='经度', y='纬度') +
                       ggtitle('站点聚类图')
cluster_map_1

cluster_map_loc <- ggmap(my_map) + 
                         geom_point(data = res_cluster_loc, aes(x=lon, y=lat,colour=factor(cluster)),size=3) +
                         theme(text = element_text(family = 'STKaiti')) +
                         labs(x='经度', y='纬度') +
                         ggtitle('站点聚类图(根据地理位置)')
cluster_map_loc


