import numpy as np 
from sklearn.decomposition import NMF 
import pandas as pd 

data = [
    [5,4,1,1,3],
    [3,2,1,3,1],
    [3,3,3,3,5],
    [1,1,5,4,4],
]
columns = ['Titanic', 'Tiffany', 'Terminator', 'Star Trek','Star Wars']
index = ['Ada', 'Bob', 'Steve','Margaret']

R = pd.DataFrame(data,index=index, columns=columns).values

model = NMF(n_components=3,init='random',random_state=10)

model.fit(R)

Q=model.components_

P=model.transform(R)

print(model.reconstruction_err_)

nR = np.dot(P,Q)
print(nR)

query = [[1,2,5,4,5]]

print(model.transform(query))