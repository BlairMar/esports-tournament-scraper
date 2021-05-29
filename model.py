#%%
import pandas as pd
from sklearn import preprocessing
from data_process import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
import random
import numpy as np
import statsmodels.formula.api as smf
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

final_frame = pd_get()
y = final_frame.pop('Gain')
print(final_frame)

X_train, X_test, Y_train, Y_test = train_test_split(final_frame, y, test_size=0.3, random_state=3)
X_test, X_validation, Y_test, Y_validation = train_test_split(X_test, Y_test, test_size=0.5, random_state=3)

model = LinearRegression(normalize=True)
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
Test_Error = MSE(Y_test, Y_pred)
print(model.score(X_train, Y_train))
print(Y_pred[:5], Y_train[:5])
print(Test_Error)

# %%
