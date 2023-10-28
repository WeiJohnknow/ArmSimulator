import numpy as np
pi = np.pi

Mat4X4 = np.array([[5,0,0,0],
                   [6,1,0,0],
                   [7,0,1,0],
                   [0,0,0,1]])


J = np.zeros((12,6))


J[:,0] = Mat4X4[:3,:].T.reshape(-1)

print(Mat4X4[:3,:].T)
print(Mat4X4[:3,:].T.reshape(-1))
print(J)
