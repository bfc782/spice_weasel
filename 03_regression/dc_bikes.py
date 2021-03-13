import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

import seaborn as sns
import matplotlib.pyplot as plt

data = "./data/"
hour = "hour.csv"
df_raw = pd.read_csv(data + hour, parse_dates=True, index_col=1)
df_raw = df_raw.drop(["casual","registered"],axis=1)
df_raw.sort_values('instant')

#group data into years (thus being able to plot Y,M,D better for EDA)
Xtrain = df_raw[df_raw['yr']==0]
ytrain = df_raw[df_raw['yr']==0]['cnt']
Xtest = df_raw[df_raw['yr']==1]
ytest = df_raw[df_raw['yr']==1]['cnt']

Xtrain_day = Xtrain[(Xtrain['hr']-Xtrain['season']>=4)&(Xtrain['hr']+Xtrain['season']<=21)]


Xtrain_day['24hdtemp'] = Xtrain_day['temp'].rolling(24).mean().fillna(method='bfill')
Xtrain_day['24hdhum'] = Xtrain_day['hum'].rolling(24).mean().fillna(method='bfill')

print(Xtrain_day[['instant','season','mnth','hr','weekday','temp','hum','cnt']].head(48))

corr_matrix = Xtrain_day.corr()
print(corr_matrix['cnt'].sort_values(ascending=False))

#objective:
###1) we are interested in predicting when there will be surging demand in the network
###2) we do not mind being wrong by a few bikes in low usage times
###3) we will focus on making decent predictions for daytime operations

#hypotheses:
###1) daytime hour temperature is more important than 24hour - let's average that
###2) daytime hours are important for the weekend
###3) commuting hours are important for the weekdays

#to do:
###1) determine, define relevant categorical columns
#### weekday
###2) groupby humidity
