import numpy as np
c = np.cos
s = np.sin
pi = np.pi
d2r = np.deg2rad
r2d = np.rad2deg
class Matrix4x4:
    def __init__(self):
        
        self.org_pos = np.eye(4)

    # def RotaX(self,deg):
    #     rad = d2r(deg)
    #     rot = np.eye(4)
    #     rot[1, 1] = c(rad)
    #     rot[2, 1] = s(rad)
    #     rot[1, 2] = -s(rad)
    #     rot[2, 2] = c(rad)

    #     return rot

    # def RotaY(self, deg):
    #     rad = d2r(deg)
    #     rot = np.eye(4)
    #     rot[0, 0] = c(rad)
    #     rot[2, 0] = -s(rad)
    #     rot[0, 2] = s(rad)
    #     rot[2, 2] = c(rad)

    #     return rot

    # def RotaZ(self, deg):
    #     rad = d2r(deg)
    #     rot = np.eye(4)
    #     rot[0, 0] = c(rad)
    #     rot[1, 0] = s(rad)
    #     rot[0, 1] = -s(rad)
    #     rot[1, 1] = c(rad)

    #     return rot
    def RotaX(self,rad):
        rot = np.eye(4)
        rot[1, 1] = c(rad)
        rot[2, 1] = s(rad)
        rot[1, 2] = -s(rad)
        rot[2, 2] = c(rad)

        return rot

    def RotaY(self, rad):
        rot = np.eye(4)
        rot[0, 0] = c(rad)
        rot[2, 0] = -s(rad)
        rot[0, 2] = s(rad)
        rot[2, 2] = c(rad)

        return rot

    def RotaZ(self, rad):
        rot = np.eye(4)
        rot[0, 0] = c(rad)
        rot[1, 0] = s(rad)
        rot[0, 1] = -s(rad)
        rot[1, 1] = c(rad)

        return rot

    def RotaXYZ(self, rx, ry, rz):
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
Mat = Matrix4x4()
# test1 = Mat.RotaXYZ(pi/2,pi/4,pi/2)
# print(test1)

# test2 = Mat.EulAngle_ZYX(test1)
# print(test2)
