import math
import numpy as np


class Matrix3D:
    """
    A class for linear transformations in three dimensions.
    """
    SIZE = 4

    def __init__(self):
        """
        Create an instance of the class Matrix3D
        """
        self.mat = np.identity(self.SIZE)

    def check_identity(self):
        """
        Check if this matrix is the identity matrix.
        :return: True if this matrix is the identity matrix, False otherwise.
        """

        identity = np.identity(self.SIZE)
        return np.allclose(self.mat, identity)

    def set_identity(self):
        """
        Set this matrix to be the identity.
        """
        self.mat = np.identity(4)

    def set_mat_move(self, dx, dy, dz):
        """
        Set this matrix to a movement transformation.
        :param dx: The distance to move on the x axis.
        :param dy: The distance to move on the y axis.
        :param dz: The distance to move on the z axis.
        """

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

    def set_mat_scale(self, dx, dy, dz, xx, xy, xz):
        """
        Set this matrix to a scale transformation.
        :param dx: The center x coordinate.
        :param dy: The center y coordinate.
        :param dz: The center z coordinate.
        :param xx: The x scale factor.
        :param xy: The y scale factor.
        :param xz: The z scale factor.
        """
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

    def set_mat_rotate_x(self, angle):
        """
        Set this matrix to a rotation transformation on the x axis.
        :param angle: The angle to rotate.
        """
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = math.cos(angle)
        self.mat[1][2] = math.sin(angle)
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = -math.sin(angle)
        self.mat[2][2] = math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0

    def set_mat_rotate_x_fix(self, angle, dx, dy, dz):
        """
        Set this matrix to a rotation transformation on the x axis around a
        point.
        :param angle: The angle to rotate.
        :param dx: The center x coordinate.
        :param dy: The center y coordinate.
        :param dz: The center z coordinate.
        """
        # Move so that the center point is on (0,0,0), then rotate, then move
        # back:
        mat1 = Matrix3D()
        mat1.set_mat_move(-dx, -dy, -dz)
        self.mat[0][0] = 1.0
        self.mat[0][1] = 0.0
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = math.cos(angle)
        self.mat[1][2] = math.sin(angle)
        self.mat[1][3] = 0.0
        self.mat[2][0] = 0.0
        self.mat[2][1] = -math.sin(angle)
        self.mat[2][2] = math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        mat1.mull_mat_mat(self)
        self.set_mat_move(dx, dy, dz)
        mat1.mull_mat_mat(self)
        self.mat = mat1.mat

    def set_mat_rotate_z(self, angle):
        """
        Set this matrix to a rotation transformation on the z axis.
        :param angle: The angle to rotate.
        """
        self.mat[0][0] = math.cos(angle)
        self.mat[0][1] = math.sin(angle)
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = -math.sin(angle)
        self.mat[1][1] = math.cos(angle)
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

    def set_mat_rotate_z_fix(self, angle, dx, dy, dz):
        """
        Set this matrix to a rotation transformation on the z axis around a
        point.
        :param angle: The angle to rotate.
        :param dx: The center x coordinate.
        :param dy: The center y coordinate.
        :param dz: The center z coordinate.
        """
        # Move so that the center point is on (0,0,0), then rotate, then move
        # back:
        mat1 = Matrix3D()
        mat1.set_mat_move(-dx, -dy, -dz)
        self.mat[0][0] = math.cos(angle)
        self.mat[0][1] = math.sin(angle)
        self.mat[0][2] = 0.0
        self.mat[0][3] = 0.0
        self.mat[1][0] = -math.sin(angle)
        self.mat[1][1] = math.cos(angle)
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
        mat1.mull_mat_mat(self)
        self.set_mat_move(dx, dy, dz)
        mat1.mull_mat_mat(self)
        self.mat = mat1.mat

    def set_mat_rotate_y(self, angle):
        """
        Set this matrix to a rotation transformation on the y axis.
        :param angle: The angle to rotate.
        """
        self.mat[0][0] = math.cos(angle)
        self.mat[0][1] = 0.0
        self.mat[0][2] = math.sin(angle)
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = -math.sin(angle)
        self.mat[2][1] = 0.0
        self.mat[2][2] = math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0

    def set_mat_rotate_y_fix(self, angle, dx, dy, dz):
        """
        Set this matrix to a rotation transformation on the y axis around a
        point.
        :param angle: The angle to rotate.
        :param dx: The center x coordinate.
        :param dy: The center y coordinate.
        :param dz: The center z coordinate.
        """
        # Move so that the center point is on (0,0,0), then rotate, then move
        # back:
        mat1 = Matrix3D()
        mat1.set_mat_move(-dx, -dy, -dz)
        self.mat[0][0] = math.cos(angle)
        self.mat[0][1] = 0.0
        self.mat[0][2] = math.sin(angle)
        self.mat[0][3] = 0.0
        self.mat[1][0] = 0.0
        self.mat[1][1] = 1.0
        self.mat[1][2] = 0.0
        self.mat[1][3] = 0.0
        self.mat[2][0] = -math.sin(angle)
        self.mat[2][1] = 0.0
        self.mat[2][2] = math.cos(angle)
        self.mat[2][3] = 0.0
        self.mat[3][0] = 0.0
        self.mat[3][1] = 0.0
        self.mat[3][2] = 0.0
        self.mat[3][3] = 1.0
        mat1.mull_mat_mat(self)
        self.set_mat_move(dx, dy, dz)
        mat1.mull_mat_mat(self)
        self.mat = mat1.mat

    def set_mat_rotate_axis(self, x1, y1, z1, x2, y2, z2, teta):
        """
        Set this matrix for a rotation around a specific axis.
        :param x1: The x coordinate of one point on the axis.
        :param y1: The y coordinate of one point on the axis.
        :param z1: The z coordinate of one point on the axis.
        :param x2: The x coordinate of another point on the axis.
        :param y2: The y coordinate of another point on the axis.
        :param z2: The z coordinate of another point on the axis.
        :param teta: The angle to rotate.
        """

        m1 = Matrix3D()

        a = x2 - x1
        b = y2 - y1
        c = z2 - z1
        l = float(math.sqrt(a * a + b * b + c * c))
        a = a / l
        b = b / l
        c = c / l
        d = float(math.sqrt(b * b + c * c))

        if d == 0:
            self.set_mat_rotate_x_fix(teta, x1, y1, z1)
        else:
            self.set_mat_move(-x1, -y1, -z1)

        m1.set_identity()  # x axis
        m1.mat[1][1] = c / d
        m1.mat[1][2] = b / d
        m1.mat[2][1] = -b / d
        m1.mat[2][2] = c / d
        self.mull_mat_mat(m1)

        m1.set_identity()  # y axis
        m1.mat[0][0] = d
        m1.mat[0][2] = a
        m1.mat[2][0] = -a
        m1.mat[2][2] = d
        self.mull_mat_mat(m1)

        m1.set_mat_rotate_z(teta)  # Z axis
        self.mull_mat_mat(m1)

        m1.set_identity()  # y axis
        m1.mat[0][0] = d
        m1.mat[0][2] = -a
        m1.mat[2][0] = a
        m1.mat[2][2] = d
        self.mull_mat_mat(m1)

        m1.set_identity()  # x axis
        m1.mat[1][1] = c / d
        m1.mat[1][2] = -b / d
        m1.mat[2][1] = b / d
        m1.mat[2][2] = c / d
        self.mull_mat_mat(m1)

        m1.set_mat_move(x1, y1, z1)
        self.mull_mat_mat(m1)

    def mull_mat_mat(self, a_mat):
        """
        Multiply this matrix by another matrix from the right.
        :param a_mat: An object of type Matrix3D.
        """
        matmul = np.matmul(self.mat, a_mat.mat)
        self.mat = matmul

    def mull_all_points(self, xr, yr, zr, aNum):
        """
        Multiply a bunch of vectors by the matrix.
        :param xr: All the x coords.
        :param yr: All the y coords.
        :param zr: All the z coords.
        :param aNum: The vectors' length.
        :return: The multiplied vectors.
        """
        cr = [1 for i in range(aNum)]
        points = [xr, yr, zr, cr]
        mat = self.mat
        points = np.matmul(np.transpose(points), mat)
        points = np.transpose(points)
        xr, yr, zr, cr = points
        return points[:-1]



class Point3D:
    """
    A class for a point in 3D space.
    """
    DIMENSION = 3

    def __init__(self, x, y, z):
        """
        Create an instance of the class Point3D
        :param x: The point's x coords.
        :param y: The point's y coords.
        :param z: The point's z coords.
        """
        self.x = x
        self.y = y
        self.z = z

    def mull_point(self, mat):
        """
        Multiply the point by a matrix.
        :param mat: A matrix to multiply by.
        """
        self.x, self.y, self.z = mat.mull_all_points([self.x], [self.y],
                                                     [self.z], 1)
        self.x = float(self.x)
        self.y = float(self.y)
        self.z = float(self.z)

    def get_points(self):
        """
        :return: A tuple with all three coordinates.
        """
        return self.x, self.y, self.z
