from .shapes import Shapes
from .matrix_3D import Point3D


class Board:
    def __init__(self, magoz, light_source, color):
        self.side_a = Shapes(magoz, light_source, 'ex12/SideA.obj', color,
                             'boardA')
        self.side_b = Shapes(magoz, light_source, 'ex12/SideB.obj', color,
                             'boardB')

    def build_shape(self, x, y, z):
        self.side_a.build_shape(x, y, z)
        self.side_b.build_shape(x, y, z)

    def real_to_guf(self):
        self.side_a.real_to_guf()
        self.side_b.real_to_guf()

    def mull_points(self, mat):
        self.side_a.mull_points(mat)
        self.side_b.mull_points(mat)

    def convert_and_show_back(self, canvas):
        back = max(self.side_a, self.side_b,
                   key=lambda value: value.get_big_z())
        back.convert_and_show(canvas)

    def convert_and_show_front(self, canvas):
        front = min(self.side_a, self.side_b,
                    key=lambda value: value.get_big_z())
        front.convert_and_show(canvas)

    def get_big_x(self, x=None):
        return max(self.side_a.get_big_x(), self.side_b.get_big_x())

    def get_small_x(self, x=None):
        return min(self.side_a.get_small_x(), self.side_b.get_small_x())

    def get_big_y(self, x=None):
        return max(self.side_a.get_big_y(), self.side_b.get_big_y())

    def get_small_y(self, x=None):
        return min(self.side_a.get_small_y(), self.side_b.get_small_y())

    def get_big_z(self, x=None):
        return max(self.side_a.get_big_z(), self.side_b.get_big_z())

    def get_small_z(self, x=None):
        return min(self.side_a.get_small_z(), self.side_b.get_small_z())

    def get_middle(self):
        a1, b1, c1 = self.side_b.get_middle().get_points()
        a2, b2, c2 = self.side_a.get_middle().get_points()
        x = (a1 + a2) / 2
        y = (b1 + b2) / 2
        z = (c1 + c2) / 2
        return Point3D(x, y, z)
