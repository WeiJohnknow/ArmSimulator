import numpy as np
from Matrix import Matrix4x4

class Quaternion:
    def __init__(self) -> None:
        pass

    def RotaMat_To_Quaternion(self, Mat3x3):
        """convert Quaternion and Rotation Matrix

        Args:
        - Rotation Matrix 3x3 .

        Return: 
        - q = a + bi + cj + dk 
        """

        sin = np.sin
        cos = np.cos
        acos = np.arccos

        θ = acos((Mat3x3[0, 0]+Mat3x3[1, 1]+Mat3x3[2, 2]-1)/2)
        if sin(θ) != 0:
            kx = (Mat3x3[2, 1] - Mat3x3[1, 2]) / (2*sin(θ))
            ky = (Mat3x3[0, 2] - Mat3x3[2, 0]) / (2*sin(θ))
            kz = (Mat3x3[1, 0] - Mat3x3[0, 1]) / (2*sin(θ))
        else:
            kx = 0
            ky = 0
            kz = 0

        a = cos(θ/2)
        b = kx * sin(θ/2)
        c = ky * sin(θ/2)
        d = kz * sin(θ/2)

        quaternion = np.array([a, b, c, d])

        return quaternion
    
    def Quaternion_To_RotaMat(self, quaternion):
        """
        Convert quaternion to rotation matrix.

        Parameters:
        - q: 1D NumPy array representing the quaternion [a, b, c, d].

        Returns:
        - 3x3 NumPy array representing the rotation matrix.
        """

        a, b, c, d = quaternion

        rotation_matrix = np.array([
            [a**2 + b**2 - c**2 - d**2, 2 * (b*c - a*d), 2 * (b*d + a*c), 0],
            [2 * (b*c + a*d), a**2 - b**2 + c**2 - d**2, 2 * (c*d - a*b), 0],
            [2 * (b*d - a*c), 2 * (c*d + a*b), a**2 - b**2 - c**2 + d**2, 0],
            [0, 0, 0, 1]
        ])

        return rotation_matrix


Mat = Matrix4x4()
crt = Quaternion()
d2r = np.deg2rad

Rmatx90 = Mat.RotaX(d2r(90)) 
Rmaty90 = Mat.RotaY(d2r(90))
Rmatz90 = Mat.RotaZ(d2r(90))

Nowpos = np.eye(4)
Goalpos = Rmatx90 @ Rmaty90 @ Rmatz90



quaternion = crt.RotaMat_To_Quaternion(Goalpos)

print("Quaternion:", quaternion)
RotaMat = crt.Quaternion_To_RotaMat(quaternion)
print(RotaMat)

        