# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import pdb
from sklearn.ensemble import GradientBoostingRegressor  #GBM algorithm
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search

import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
# from rpy2 import robjects

# R = robjects.r

# rsrcipts = '''
#     dat = read.csv("..//data//model_32.csv")
#     dat$weekday = as.factor(dat$weekday)
#     dat$sunny   = as.factor(dat$sunny)
#     dat$windy   = as.factor(dat$windy)
#     dat$hour    = as.factor(dat$hour)
#     x = model.matrix(count ~ . - date, data = dat)[, -1]
#     x
# '''

# resx = R(rsrcipts)


def add_zero(string):
    return (10 - len(string)) * '0' + string

def modelfit(alg, dtrain, predictors, dtest=None, performCV=True, printFeatureImportance=True, cv_folds=5):
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain[target])
        
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    # dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
    # dtrian_r2 = alg.score(d)
    
    #Perform cross-validation:
    if performCV:
        cv_score = cross_validation.cross_val_score(alg, dtrain[predictors], dtrain[target], cv=cv_folds, scoring='mean_squared_error')
    
    #Print model report:
    pdb.set_trace()
    print("\nModel Report")
    print("MSE : %.4g" % metrics.accuracy_score(dtrain[target].values, dtrain_predictions))
    # print("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain[target], dtrain_predprob))
    
    if performCV:
        print("CV Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))
        
    #Print Feature Importance:
    if printFeatureImportance:
        feat_imp = pd.Series(alg.feature_importances_, predictors).sort_values(ascending=False)
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importance Score')
        plt.show()
    
    if dtest is None:
        print("\nDo not have target data")
    else:
        dtest_predictions = alg.predict(dtest[predictors])
        dtest_predprob = alg.predict_proba(dtest[predictors])[:,1]
        dtest_num = dtest.index
        
        res = list(zip(dtest_num, dtest_predictions, dtest_predprob))
        print("target head:")
        print(res[:10])
        
        print("sorted res:")
        final_res = sorted(res, key = lambda x: x[2], reverse = True)
        print(final_res[:10])
        
        fw = open('result_gbdt.csv', 'w')
        for num, _, _ in final_res:
            fw.write(add_zero(str(num)) + '\n')

df = pd.read_csv("../data/model_32.csv")
# df_test = pd.read_csv("test_res.csv", index_col = 0)

target = 'count'
predictors = [x for x in df.columns if x not in [target, 'date']]

#param_test = {
#    #'n_estimators': list(range(20, 101, 10)),
#    #'max_depth': list(range(15, 26, 2)),
#    #'min_samples_split': list(range(200, 1001, 200)),
#    #'min_samples_leaf': list(range(30, 71, 10))
#    #'max_features': list(range(3, 12, 2))
#    #'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9]
#}
#gsearch = GridSearchCV(estimator = GradientBoostingRegressor(
#    learning_rate = 0.1,
#    n_estimators = 80,
#    min_samples_split = 800,
#    min_samples_leaf = 60,
#    max_depth = 13,
#    max_features = 7,
#    subsample = 0.8,
#    random_state = 418
#    ),
#    param_grid = param_test,
#    scoring = 'accuracy',
#    cv = 7,
#    iid = False,
#    )
#gsearch.fit(df[predictors], df[target])
#print(gsearch.grid_scores_)
#print(gsearch.best_params_)
#print(gsearch.best_score_)

gbm0 = GradientBoostingRegressor(
    loss = 'ls',
    # criterion = 'friedman_mse',
    learning_rate = 0.05,
    n_estimators = 200,
    min_samples_split = 800,
    min_samples_leaf = 60,
    max_depth = 13,
    max_features = 'auto',
    subsample = 0.8,
    random_state = 418
    )
# modelfit(gbm0, df, predictors, dtest = df_test)
modelfit(gbm0, df, predictors, dtest = None)