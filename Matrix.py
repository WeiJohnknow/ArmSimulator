import numpy as np
c = np.cos
s = np.sin
pi = np.pi
d2r = np.deg2rad
r2d = np.rad2deg
class Matrix4x4:
    def __init__(self):
        pass

    def RotaX(self, rad):
        """
        Unit : radian
        """
        rot = np.eye(4)
        rot[1, 1] = c(rad)
        rot[2, 1] = s(rad)
        rot[1, 2] = -s(rad)
        rot[2, 2] = c(rad)

        return rot

    def RotaY(self, rad):
        """
        Unit : radian
        """
        rot = np.eye(4)
        rot[0, 0] = c(rad)
        rot[2, 0] = -s(rad)
        rot[0, 2] = s(rad)
        rot[2, 2] = c(rad)

        return rot

    def RotaZ(self, rad):
        """
        Unit : radian
        """
        rot = np.eye(4)
        rot[0, 0] = c(rad)
        rot[1, 0] = s(rad)
        rot[0, 1] = -s(rad)
        rot[1, 1] = c(rad)

        return rot

    def RotaXYZ(self, rx, ry, rz):
        """
        Fixed Angle
        """
        Rx = self.RotaX(rx)
        Ry = self.RotaY(ry)
        Rz = self.RotaZ(rz)
        # Rot = Rx @ Ry @ Rz
        Rot = Rz @ Ry @ Rx #fixed angle 先轉的後乘，前乘會變動到基礎坐標系

        return Rot

    def TransXYZ(self, x, y, z):
        Trans = np.eye(4)
        Trans[0,3] = x
        Trans[1,3] = y
        Trans[2,3] = z
        
        return Trans
        
    def EulAngle_ZYX(self, TransformationMat): 
        
        #fixed angle xyz =>euler use zyx method

        r11 = TransformationMat[0,0]
        r21 = TransformationMat[1,0]
        r31 = TransformationMat[2,0]

        r12 = TransformationMat[0,1]
        r22 = TransformationMat[1,1]
        r32 = TransformationMat[2,1]

        r13 = TransformationMat[0,2]
        r23 = TransformationMat[1,2]
        r33 = TransformationMat[2,2]

        if r11 == 0 and r21 == 0:
            β_rad = np.pi/2
            α_rad = 0
            γ_rad = np.arctan2(r12, r22)
        else:
            β_rad = np.arctan2(-r31,np.sqrt(np.square(r11)+np.square(r21)))
            α_rad = np.arctan2(r21, r11)
            γ_rad = np.arctan2(r32, r33)
        
        Px = TransformationMat[0, 3]
        Py = TransformationMat[1, 3]
        Pz = TransformationMat[2, 3]
        γ = r2d(γ_rad)
        β = r2d(β_rad)
        α = r2d(α_rad)
        q = [Px, Py, Pz, γ, β, α]
        return q

    def MatToAngle(self, coord):
        """
        Convert Transformation matrix(4x4) to Pose matrix(6x1)
        """
        # Use Euler Angle ZYX
        q = np.zeros(shape=(6))
        r11 = coord[0,0]#Xx
        r21 = coord[1,0]#Xy
        r31 = coord[2,0]#Xz

        r12 = coord[0,1]#Yx
        r22 = coord[1,1]#Yy

        r32 = coord[2,1]#Yz
        r33 = coord[2,2]#ZZ

        β = np.arctan2(-r31,np.sqrt(r11 * r11+r21 * r21))
        alpha = 0
        gamma = 0
        if abs(β) != pi/2:
            alpha = np.arctan2(r21/np.cos(β),r11/np.cos(β))
            gamma = np.arctan2(r32/np.cos(β),r33/np.cos(β))
        else:
            if β == pi/2:
                alpha = 0
                gamma = np.arctan2(r12,r22)  
            elif  β == -pi/2:
                alpha = 0
                gamma = -np.arctan2(r12,r22) 

        # gamma -> x axis angle
        # beta  -> y axis angle
        # alpha -> z axis angle
        q = [coord[0,3], coord[1,3], coord[2,3], gamma ,β  ,alpha ]
        return q
    

    def AngletoMat(self, inputMat):
        """
        Convert matrix(6x1) to Pose Transformation matrix(4x4)
        """
        coord = np.eye(4)
        Buffer = np.eye(3)
        coord[0,3] = inputMat[0,0] 
        coord[1,3] = inputMat[1,0]
        coord[2,3] = inputMat[2,0]
        # Buffer = self.RotaX(inputMat[3,0]) @ self.RotaY(inputMat[4,0]) @ self.RotaZ(inputMat[5,0])

        # Fix Angle XYZ ➜ Euler Angle ZYX
        Buffer = self.RotaZ(inputMat[5,0]) @ self.RotaY(inputMat[4,0]) @ self.RotaX(inputMat[3,0])
        # Buffer = self.RotaX(inputMat[3,0]) @ self.RotaY(inputMat[4,0]) @ self.RotaZ(inputMat[5,0])
        coord[:3,0] = Buffer[:3,0]
        coord[:3,1] = Buffer[:3,1]
        coord[:3,2] = Buffer[:3,2]


        return coord
    

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
            [a**2 + b**2 - c**2 - d**2, 2 * (b*c - a*d), 2 * (b*d + a*c)],
            [2 * (b*c + a*d), a**2 - b**2 + c**2 - d**2, 2 * (c*d - a*b)],
            [2 * (b*d - a*c), 2 * (c*d + a*b), a**2 - b**2 - c**2 + d**2]])

        return rotation_matrix


Mat = Matrix4x4()
world_coordinate = np.eye(4)
Ap = world_coordinate

# deg = 90
# for i in range(2):
    
#     q = Mat.RotaMat_To_Quaternion(Mat.RotaZ(d2r(deg)))
#     print(q)
#     r = Mat.Quaternion_To_RotaMat(q)
#     print(r)
#     deg += 1

# 四元數差值
Now = np.eye(3)
Goal= np.array([[ 0, -1,  0],
                       [ 1,  0,  0],
                       [ 0,  0,  1]])
qNow = Mat.RotaMat_To_Quaternion(Now)
qGoal = Mat.RotaMat_To_Quaternion(Goal)
dw = (qGoal[0]-qNow[0])/100
dk = (qGoal[3]-qNow[3])/100

print(qNow)
print(qGoal)
print(dw)
print(dk)

