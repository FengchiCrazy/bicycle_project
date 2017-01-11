setwd("~/Github/bicycle_project/new_york/code/")

week_list = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun")
dat = read.csv("pred.csv")
anyNA(dat)
dat = na.omit(dat)
dat

dat$year = as.factor(dat$year)
dat$month = as.factor(dat$month)
dat$weekday = as.factor(dat$weekday)
# dat$sunny   = as.factor(dat$sunny)
# #dat$windy   = as.factor(dat$windy)
# 
# dat$hour    = as.factor(dat$hour)
# str(dat)

library(xgboost)

xgb_dat = model.matrix(count ~ . - day, dat)[, -1]
n = dim(xgb_dat)[1]

train_boundary = round(n * 0.7, 0)
# x_train = xgb_dat[1:train_boundary,]
# x_test  = xgb_dat[(train_boundary + 1):n,]
# y_train = dat$count[1:train_boundary]
# y_test  = dat$count[(train_boundary + 1): n]

set.seed(418)
sample_index = sample(n, train_boundary, replace = F)

x_train = xgb_dat[sample_index,]
x_test  = xgb_dat[-sample_index,]
y_train = dat$count[sample_index]
y_test  = dat$count[-sample_index]

library(caret)

caret_data = data.frame(cbind(dat$count, xgb_dat))

fit_control = trainControl(method = "repeatedcv",
                           number = 5,
                           repeats = 5)
set.seed(418)
xgb_grid = expand.grid(max_depth = c(1, 3, 5, 9),
                       eta = 1:5 * 0.1,
                       nrounds = 1:3 * 100,
                       gamma = 7:10 * 0.1,
                       colsample_bytree = 0.8,
                       min_child_weight = 1,
                       subsample = 1
)
xgb_fit = train(V1 ~ ., caret_data,
                method = "xgbTree",
                trControl = fit_control,
                tuneGrid = xgb_grid,
                verbose = 1)

xgb_fit
xgb_fit$bestTune

plot(xgb_fit)


# xgb trainning
dtrain = xgb.DMatrix(data = x_train[,-1], label = y_train)
dtest  = xgb.DMatrix(data = x_test[,-1], label  = y_test)

watch_list = list(train = dtrain, test = dtest)

bst <- xgb.train(data=dtrain, max.depth=5, 
                 eta=0.1, nthread = 2, nrounds=500,
                 colsample_bytree = 0.8,
                 gamma = 0.8,
                 watchlist=watch_list, 
                 objective = "reg:linear")
plot(bst)
pred = predict(bst, dtest)
plot(pred,y_test)

write.table(data.frame(pred, y_test), file = "xgb_pred_sample.csv", sep = ',', row.names = FALSE, col.names = TRUE)


