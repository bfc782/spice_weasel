import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

#plt.rcParams('figure.figsize') = (12,6)

data = './data/'
train = 'train.csv'
test = 'test.csv'
df_train = pd.read_csv(data+train)
df_test = pd.read_csv(data+test)

df_train_num = df_train.drop(['Name','Sex','Ticket','Cabin','Embarked'],axis=1)
print(df_train_num.head())

#Encode fe/male assignments to binary gender assignments (though a modern statistical heuristic may be available for non-binary)
gender = {'female':0, 'male':1}
df_train['Gender']=df_train['Sex'].map(gender)

#One-hot-encode the embarcation points 
#emb_cat = df_train[['Embarked']]
#cat_encoder = OneHotEncoder()
#emb_cat_1hot = cat_encoder.fit_transform(emb_cat)

#print(df_train.columns,'\n',df_train.describe())

