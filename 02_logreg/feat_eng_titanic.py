#%%
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
#%%
data = './data/'
train = 'train.csv'
test = 'test.csv'
df_train = pd.read_csv(data+train)
df_test = pd.read_csv(data+test)
#%%
df_train_target = df_train['Survived']
df_train_num = df_train.drop(['Name','Survived','Sex','Ticket','Cabin','Embarked'],axis=1)
df_train_catgen = df_train[['Sex','Embarked']]
#%%
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('std_scaler', StandardScaler()),
])

#df_train_num_tr = num_pipeline.fit_transform(df_train_num)
num_attribs = list(df_train_num)

cat_pipeline = Pipeline([
    ('missing', SimpleImputer(strategy='most_frequent')),
    ('one_hot', OneHotEncoder(sparse=False, handle_unknown='ignore')),
])
cat_attribs = list(df_train_catgen)

full_pipeline = ColumnTransformer([
    ('num', num_pipeline, num_attribs),
    ('cat', cat_pipeline, cat_attribs),
])

X_train = full_pipeline.fit_transform(df_train)
y_train = df_train_target
