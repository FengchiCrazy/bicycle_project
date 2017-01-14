setwd("~/Github/bicycle_project/new_york/code/")


week_list = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun")
dat = read.csv("pred.csv")
anyNA(dat)
dat = na.omit(dat)
dat = dat[-1,]
head(dat)

dat$year = as.factor(dat$year)
dat$month = as.factor(dat$month)
dat$weekday = as.factor(dat$weekday)


library(gbm)
gbrt_dat = model.matrix(count ~ . - day, dat)[, -1]
n = dim(gbrt_dat)[1]

# build train && test dataset
train_boundary = round(n * 0.7, 0)
x_train = gbrt_dat[1:train_boundary,]
x_test  = gbrt_dat[(train_boundary + 1):n,]
y_train = dat$count[1:train_boundary]
y_test  = dat$count[(train_boundary + 1): n]

# sample train && test dataset
set.seed(418)
sample_index = sample(n, train_boundary, replace = F)

x_train = gbrt_dat[sample_index,]
x_test  = gbrt_dat[-sample_index,]
y_train = dat$count[sample_index]
y_test  = dat$count[-sample_index]

# param tune
library(caret)
set.seed(418)
caret_data = data.frame(cbind(dat$count, gbrt_dat))
fitControl <- trainControl(method = "repeatedcv", 
                           number = 5,
                           repeats = 5)
gbrt_fit <- train(V1 ~ . , data=caret_data, method='gbm',
                #distribution='guassian',
                trControl = fitControl,
                verbose = F,
                tuneGrid = expand.grid(n.trees=1:4 * 100,
                                       shrinkage= 1:5 * 0.1,
                                       interaction.depth=c(1, 3, 5, 9),
                                       n.minobsinnode = 1:4*10
                                       # distribution='guassian'
                )
)
gbrt_fit
gbrt_bestTune = gbrt_fit$bestTune
plot(gbrt_fit)
plot.gbm(gbm_r, 8, best_iter)

train_df = data.frame(cbind(x_train, y_train))
test_df  = data.frame(cbind(x_test,  y_test))

gbm_result = gbm(y_train ~ ., data = train_df,
                 n.trees = gbrt_bestTune$n.trees,
                 shrinkage = gbrt_bestTune$shrinkage, 
                 interaction.depth = gbrt_bestTune$interaction.depth,
                 bag.fraction = 0.6,
                 n.minobsinnode = gbrt_bestTune$n.minobsinnode,
                 cv.folds = 5,
                 train.fraction = 0.7
                 )


summary(gbm_result, n.trees = best_iter)
plot.gbm(gbm_result, 4, best_iter)


best_iter = gbm.perf(gbm_result, method = "OOB")
print(best_iter)
pred = predict(gbm_result, test_df[,-length(colnames(test_df))], best_iter)
write.table(data.frame(pred, y_test), file = "gbm_res.csv", sep = ',', row.names = FALSE, col.names = TRUE)


MSE = mean((pred - y_test) ^ 2)

final_df = data.frame(true = dat$count, pred = pred)
dat$pred = pred

plot(y = dat[(dat$hour %in% c( 8)),]$count,  x = as.Date(as.character(dat[(dat$hour %in% c( 8)),]$date), "%Y%m%d"), type="l", xlab = "date", ylab = "count", col = "red")
lines(y = dat[(dat$hour %in% c( 8)),]$pred,  x = as.Date(as.character(dat[(dat$hour %in% c( 8)),]$date), "%Y%m%d"), type="l", xlab = "date", ylab = "count", col = "blue")
write.table(dat, file = "res.csv", sep = ',', row.names = FALSE, col.names = TRUE)
