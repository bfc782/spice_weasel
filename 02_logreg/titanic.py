#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import plot_confusion_matrix, f1_score, precision_score, recall_score, precision_recall_curve, roc_curve

#plt.rcParams('figure.figsize') = (12,6)

def nan_rows(df,csv_eda="False"):
    is_NaN = df.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = df[row_has_NaN]
    if csv_eda:
        rows_with_NaN.to_csv(f'./eda/{df.name}_with_nan.csv',index=True)
    else:    
        return rows_with_NaN

data = './data/'
train = 'train.csv'
test = 'test.csv'
df_train = pd.read_csv(data+train)
df_test = pd.read_csv(data+test)
#%%
#EDA shows very few Embarked NaN - choosing to drop these for the moment.
df_train = df_train.dropna(subset=['Embarked'])
df_test = df_test.dropna(subset=['Embarked'])

df_train_target = df_train['Survived']
df_train_num = df_train.drop(['Name','Survived','Sex','Ticket','Cabin','Embarked'],axis=1)
df_train_num.name = 'numerical_data'

#NOTE: at this point we consider how to treat the numerical NaNs - most appear on age 
## a) drop them - there are 177 - almost 20%, too many to drop
## b) simple imputation, e.g. median - this seems too simplistic but that's our starting point
## c) compare the survival rate of unknown ages to the known age buckets. create a stratified imputation - this is more costly but should yield better predictive powers

imputer = SimpleImputer(strategy='median')
imputer.fit(df_train_num)
X = imputer.transform(df_train_num)
#df_train_tr = pd.DataFrame(X,columns=df_train_num.columns,index=df_train_num.index)

df_train_cat = df_train[['Name','Sex','Ticket','Cabin','Embarked']]
df_train_cat.name = 'categorical_data'
#nan_rows(df_train_cat) #output to eda folder - most are for cabin, some are for embarked

#Encode fe/male assignments to binary gender assignments (though a modern statistical heuristic may be available for non-binary)
# gender = {'female':0, 'male':1}
# df_train_cat['Sex']=df_train_cat['Sex'].map(gender)

#One-hot-encode the embarcation points 
##df_name_emb = df_train_cat[['Name','Embarked']]
##df_name_emb.name = 'embarked'
##nan_rows(df_name_emb) #only 2 embarkations missing from rawtrain data so going to drop these in the file read stage
emb_cat = df_train_cat[['Embarked']]
emb_cat.name = 'emb_cat_now'
#print(nan_rows(emb_cat))
cat_encoder = OneHotEncoder()
emb_cat_1hot = cat_encoder.fit_transform(emb_cat)
#%%
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('std_scaler', StandardScaler()),
  ])

#df_train_num_tr = num_pipeline.fit_transform(df_train_num)
num_attribs = list(df_train_num)
sex_enc = ['Sex']
emb_enc = ['Embarked']
#%%
full_pipeline = ColumnTransformer([
    ('num', num_pipeline, num_attribs),
    ('sex', OneHotEncoder(), sex_enc),
    ('emb', OneHotEncoder(), emb_enc),
  ])

X_train = full_pipeline.fit_transform(df_train)
y_train = df_train_target

# %%
m = LogisticRegression(random_state=337)
m.fit(X_train, y_train)
m.score(X_train, y_train)

# %%
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
# %%

print(f'precision for survival predict:{round(precision_score(y_train, m.predict(X_train), pos_label=1),2)}')

print(f'recall for survival predict:{round(recall_score(y_train, m.predict(X_train), pos_label=1),2)}')

print(f'f1_score for survival predict:{round(f1_score(y_train, m.predict(X_train), pos_label=1),2)}')

# %%

print(f'precision for perished predict:{round(precision_score(y_train, m.predict(X_train), pos_label=0),2)}')

print(f'recall for perished predict:{round(recall_score(y_train, m.predict(X_train), pos_label=0),2)}')

print(f'f1_score for perished predict:{round(f1_score(y_train, m.predict(X_train), pos_label=0),2)}')

# %%
y_scores = cross_val_predict(m, X_train, y_train, cv=5, method='decision_function')
precisions, recalls, thresholds = precision_recall_curve(y_train, y_scores)

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
  plt.plot(thresholds, precisions[:-1],"b--", label="Precision")
  plt.plot(thresholds, recalls[:-1],"g-", label="Recall")

plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.show()
# %%
fpr, tpr, thresholds = roc_curve(y_train, y_scores)

def plot_roc_curve(fpr, tpr, label=None):
  plt.plot(fpr, tpr, linewidth=2, label=label)
  plt.plot([0,1],[0,1],'k--')

plot_roc_curve(fpr, tpr)
plt.show
# %%
