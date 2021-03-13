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

sat_14 = (Xtrain['weekday']==6)&(Xtrain['hr']==14)
df_sat14 = Xtrain[sat_14]
df_sat14['sc_cnt'] = 0
min_cnt = df_sat14.min()
max_cnt = df_sat14.max()
denom = max_cnt - min_cnt

cnt_s = df_sat14['cnt'].copy
    
cnt_scaled = []
for i in range(len(df_sat14)):
    cnt_scaled.append((cnt_s[i]-min_cnt)/denom)

df_sat14['sca_cnt'] = cnt_scaled

df_sat14[['temp','hum','weathersit','sca_cnt']].plot()
plt.show()

#Xtrain_day = Xtrain[(Xtrain['hr']-Xtrain['season']>=4)&(Xtrain['hr']+Xtrain['season']<=21)]
#Xtrain_day['24hdtemp'] = Xtrain_day['temp'].rolling(24).mean().fillna(method='bfill')
#Xtrain_day['24hdhum'] = Xtrain_day['hum'].rolling(24).mean().fillna(method='bfill')

#print(Xtrain_day[['instant','season','mnth','hr','weekday','temp','hum','cnt']].head(48))

#corr_matrix = Xtrain_day.corr()
#print(corr_matrix['cnt'].sort_values(ascending=False))

