setwd("~/Github/bicycle_project/new_york/code/")

library(dplyr)
library(ggplot2)

des_data = read.table("describe.csv",header = TRUE,sep = ",", na.strings = "NA")
head(des_data)

des_tbl = tbl_df(des_data)
des_tbl

des_tbl %>%
  group_by(age) %>%
  summarise(total = sum(count))

