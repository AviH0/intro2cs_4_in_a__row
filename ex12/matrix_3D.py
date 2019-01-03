import math as Math


class Matrix3D:
    
    SIZE = 4
    

    
    def __init__(self):
        self.mat = [[0 for i in range(self.SIZE)] for j in range(self.SIZE)]
        self.setIdentity()

    def setIdentity(self):
            
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = 0.0
        self.mat[2][2] = 1.0
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0

    def setMatMove(self, dx,  dy,  dz):
    
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = 0.0
        self.mat[2][2] = 1.0
        self.mat[2][3] = 0.0
        self.mat[3][0] = dx
        self.mat[3][1] = dy
        self.mat[3][2] = dz
        self.mat[3][3] = 1.0

    def setMatScale(self, dx, dy, dz, xx, xy, xz):
    
        self.mat[0][0] = xx
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = xy
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = 0.0
        self.mat[2][2] = xz
        self.mat[2][3] = 0.0
        self.mat[3][0] = (1 - xx) * dx
        self.mat[3][1] = (1 - xy) * dy
        self.mat[3][2] = (1 - xz) * dz
        self.mat[3][3] = 1.0

    def setMatRotateX(self, angle):
    
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = Math.cos(angle)
        self.mat[1][2] = Math.sin(angle)
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = -Math.sin(angle)
        self.mat[2][2] = Math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        
    
    def setMatRotateXFix(self, angle, dx, dy, dz):
    
        mat1 = Matrix3D()
        mat1.setMatMove(-dx, -dy, -dz)
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = Math.cos(angle)
        self.mat[1][2] = Math.sin(angle)
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = -Math.sin(angle)
        self.mat[2][2] = Math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        mat1.mullMatMat(self)
        self.setMatMove(dx, dy, dz)
        mat1.mullMatMat(self)
        self.mat = mat1.mat
        
    
    def setMatRotateZ(self, angle):
    
        self.mat[0][0] = Math.cos(angle)
        self.mat[0][1] = Math.sin(angle)
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = -Math.sin(angle)
        self.mat[1][1] = Math.cos(angle)
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = 0.0
        self.mat[2][2] = 1.0
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        
    
    def setMatRotateZFix(self, angle, dx, dy, dz):
    
        mat1 = Matrix3D()
        mat1.setMatMove(-dx, -dy, -dz)
        self.mat[0][0] = Math.cos(angle)
        self.mat[0][1] = Math.sin(angle)
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = -Math.sin(angle)
        self.mat[1][1] = Math.cos(angle)
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = 0.0
        self.mat[2][2] = 1.0
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        mat1.mullMatMat(self)
        self.setMatMove(dx, dy, dz)
        mat1.mullMatMat(self)
        self.mat = mat1.mat
    
    
    def setMatRotateY(self, angle):
    
        self.mat[0][0] = Math.cos(angle)
        self.mat[0][1] = 0.0
        self.mat[0][2] = Math.sin(angle)
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = -Math.sin(angle)
        self.mat[2][1] = 0.0
        self.mat[2][2] = Math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
    
    
    def setMatRotateYFix(self, angle, dx, dy, dz):
    
        mat1 = Matrix3D()
        mat1.setMatMove(-dx, -dy, -dz)
        self.mat[0][0] = Math.cos(angle)
        self.mat[0][1] = 0.0
        self.mat[0][2] = Math.sin(angle)
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = -Math.sin(angle)
        self.mat[2][1] = 0.0
        self.mat[2][2] = Math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        mat1.mullMatMat(self)
        self.setMatMove(dx, dy, dz)
        mat1.mullMatMat(self)
        self.mat = mat1.mat
        
        
    def setMatRotateAxis(self, x1, y1, z1,x2, y2, z2, teta):
    
        m1 = Matrix3D()
        
        a = x2 - x1
        b = y2 - y1
        c = z2 - z1
        l = float(Math.sqrt(a * a + b * b + c * c))
        a = a / l
        b = b / l
        c = c / l
        d = float(Math.sqrt(b * b + c * c))
    
        if d == 0:
            self.setMatRotateXFix(teta, x1, y1, z1)
        else:
            self.setMatMove(-x1, -y1, -z1)
    
        m1.setIdentity() # x axis
        m1.mat[1][1] = c / d
        m1.mat[1][2] = b / d
        m1.mat[2][1] = -b / d
        m1.mat[2][2] = c / d
        self.mullMatMat(m1)
    
        m1.setIdentity() # y axis
        m1.mat[0][0] = d
        m1.mat[0][2] = a
        m1.mat[2][0] = -a
        m1.mat[2][2] = d
        self.mullMatMat(m1)
    
        m1.setMatRotateZ(teta) # Z axis
        self.mullMatMat(m1)
    
        m1.setIdentity() # y axis
        m1.mat[0][0] = d
        m1.mat[0][2] = -a
        m1.mat[2][0] = a
        m1.mat[2][2] = d
        self.mullMatMat(m1)
    
    
        m1.setIdentity() # x axis
        m1.mat[1][1] = c / d
        m1.mat[1][2] = -b / d
        m1.mat[2][1] = b / d
        m1.mat[2][2] = c / d
        self.mullMatMat(m1)
    
        m1.setMatMove(x1, y1, z1)
        self.mullMatMat(m1)

    def mullMatMat(self, a_mat):
    
        temp = Matrix3D()
        for i in range(self.SIZE):
            for j in range(self.SIZE):

                temp.mat[i][j] = 0
                for k in range(self.SIZE):
                    temp.mat[i][j] += self.mat[i][k] * a_mat.mat[k][j]

        self.mat=temp.mat

    def mullAllPoints(self, xr,  yr,  zr, aNum):
    
        for  i in range(aNum):
            xTemp=xr[i]; yTemp= yr[i]; zTemp=zr[i]
            xr[i]=xTemp * self.mat[0][0] + yTemp * self.mat[1][0] + zTemp * self.mat[2][0] + 1 * self.mat[3][0]
            yr[i]=xTemp * self.mat[0][1] + yTemp * self.mat[1][1] + zTemp * self.mat[2][1] + 1 * self.mat[3][1]
            zr[i]=xTemp * self.mat[0][2] + yTemp * self.mat[1][2] + zTemp * self.mat[2][2] + 1 * self.mat[3][2]
