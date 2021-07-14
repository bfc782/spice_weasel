#%% 
import numpy as np 
from sklearn.decomposition import NMF 
import pandas as pd 

#dummy ratings: 5 films, 4 users
data = [
    [5,4,1,1,3],
    [3,2,1,3,1],
    [3,3,3,3,5],
    [1,1,5,4,4],
]
columns = ['Titanic', 'Tiffany', 'Terminator', 'Star Trek','Star Wars']
index = ['Ada', 'Bob', 'Steve','Margaret']

#create dataframe
R = pd.DataFrame(data,index=index, columns=columns).values

#create model and set hyperparameters
#model assumes R - PQ
model = NMF(n_components=3,init='random',random_state=10)

model.fit(R)

Q=model.components_ #movie-genre matrix

P=model.transform(R) # user-genre matrix

print(model.reconstruction_err_) # reconstruction error

nR = np.dot(P,Q)
print(nR) # reconstructed matrix!

# a new data point to predict
query = [[1,2,5,4,5]]

# in
print(model.transform(query))
# %%
