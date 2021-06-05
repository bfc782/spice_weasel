#%%
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier

from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import plot_confusion_matrix, confusion_matrix, f1_score, precision_score, recall_score, precision_recall_curve, roc_curve

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
df_train_num = df_train.drop(['PassengerId','Name','Survived','Sex','Ticket','Cabin','Embarked'],axis=1)
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

#%%
models = [
          ('logreg', LogisticRegression()),
          ('tree', DecisionTreeClassifier()),
          ('forest', RandomForestClassifier(max_depth=3, n_estimators=10)),
          ('svm', SVC(kernel='rbf'))
]

m = VotingClassifier(models)
m1 = RandomForestClassifier(max_depth=3, n_estimators=10)
m.fit(X_train, y_train)
m.score(X_train, y_train)
# importances = m.feature_importances_
#%%
cross_val_acc = cross_val_score(estimator=m
                , X=X_train
                , y=y_train
                , cv=5
                , scoring='accuracy')
cross_val_acc
# %%
plot_confusion_matrix(estimator=m,
                      X=X_train,
                      y_true=y_train,
                      normalize=None)

tn, fp, fn, tp = confusion_matrix(y_train, m.predict(X_train)).ravel()
print(tn, fp, fn, tp)

# %%
