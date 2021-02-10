import numpy as np

u1 = np.array([2,4])
u2 = np.array([4,2])

numer = np.dot(u1,u2)
denom = np.sqrt(np.dot(u1,u1))*np.sqrt(u2[0]**2+u2[1]**2)

output = numer/denom
print(output)
