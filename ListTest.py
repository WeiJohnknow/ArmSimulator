import numpy as np
pi = np.pi

Mat = np.array([[1,0,0,6],
                   [0,1,0,-2],
                   [0,0,1,4],
                   [0,0,0,1]])

Buffer = np.zeros((10,3))

for i in range(3):
    Buffer[0,i] = Mat[i,3]

print(Buffer)