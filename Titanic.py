#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:15:32 2017

@author: June
"""

import numpy as np
import pandas as pd


train = pd.read_csv('.../train.csv')
y_train = train['Survived'].values

sex = pd.get_dummies(train['Sex'], drop_first = True)
pclass = pd.get_dummies(train['Pclass'], drop_first = True)
embark = pd.get_dummies(train['Embarked'], drop_first = True)
X_train = pd.concat([train,sex,pclass,embark], axis = 1)

X_train = X_train.drop(['PassengerId','Survived','Pclass','Name','Sex','Ticket','Cabin','Embarked'],axis = 1).values

from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values='NaN', strategy='mean', axis = 0)
imputer = imputer.fit(X_train[:,:])
X_train[:,:] = imputer.transform(X_train[:,:])

import statsmodels.formula.api as sm
X_train = np.append(arr = np.ones((891,1)).astype(int), values = X_train, axis = 1)

X_opt = X_train[:, [0,1,2,3,4,5,6,7,8,9]]
regressor_OLS = sm.OLS(endog= y_train, exog= X_opt).fit()
regressor_OLS.summary()
X_opt = X_train[:, [0,1,2,4,5,6,7,8,9]]
regressor_OLS = sm.OLS(endog= y_train, exog= X_opt).fit()
regressor_OLS.summary()
X_opt = X_train[:, [0,1,2,5,6,7,8,9]]
regressor_OLS = sm.OLS(endog= y_train, exog= X_opt).fit()
regressor_OLS.summary()
X_opt = X_train[:, [0,1,2,5,6,7]]
regressor_OLS = sm.OLS(endog= y_train, exog= X_opt).fit()
regressor_OLS.summary()

test = pd.read_csv('.../test.csv')
X_test = pd.concat([test, pd.get_dummies(test['Sex'], drop_first = True), pd.get_dummies(test['Pclass'], drop_first = True)], axis = 1)
X_test = X_test.drop(['PassengerId','Pclass','Name','Sex','Parch','Ticket','Fare','Cabin','Embarked'], axis = 1).values

imputer = Imputer(missing_values='NaN', strategy='mean', axis = 0)
imputer = imputer.fit(X_test[:,:])
X_test[:,:] = imputer.transform(X_test[:,:])
X_test = np.append(arr = np.ones((418,1)).astype(int), values = X_test, axis = 1)
                  
y_pred = regressor_OLS.predict(X_test)

answer = pd.read_csv('.../gender_submission.csv')
y_test = answer['Survived'].values

y_pred[y_pred >= 0.5] = 1
y_pred[y_pred < 0.5] = 0

y_pred = y_pred.astype(int)
residual = y_pred - y_test

residual[residual != 0]
