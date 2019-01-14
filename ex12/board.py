from .shapes import Shapes
from .matrix_3D import Point3D


class Board:

    # Files:
    SIDE_A_FILE = 'ex12/Main_Body_Left_Side.obj'#'ex12/SideA.obj'
    SIDE_B_FILE = 'ex12/Main_Body_Right_Side.obj'#'ex12/SideB.obj'

    # Tags:
    SIDE_A_TAG = 'boardA'
    SIDE_B_TAG = 'boardB'

    def __init__(self, magoz, light_source, color):
        self.side_a = Shapes(magoz, light_source, self.SIDE_A_FILE, color,
                             self.SIDE_A_TAG)
        self.side_b = Shapes(magoz, light_source, self.SIDE_B_FILE, color,
                             self.SIDE_B_TAG)
        self.__board_top = None
        self.__board_bottom = None

    def build_shape(self, x, y, z):
        self.side_a.build_shape(x, y, z)
        self.side_b.build_shape(x, y, z)
        self.__board_top = Point3D(self.get_middle().x,
                                   self.get_small_y(),
                                   self.get_middle().z)
        self.__board_bottom = Point3D(self.get_middle().x,
                                      self.get_big_y(),
                                      self.get_middle().z)

    def real_to_guf(self):
        self.side_a.real_to_guf()
        self.side_b.real_to_guf()

    def mull_points(self, mat):
        self.side_a.mull_points(mat)
        self.side_b.mull_points(mat)
        self.__board_top.mull_point(mat)
        self.__board_bottom.mull_point(mat)

    def convert_and_show_back(self, canvas):
        back = max(self.side_a, self.side_b,
                   key=lambda value: value.get_big_z())
        back.convert_and_show(canvas)

    def convert_and_show_front(self, canvas):
        front = min(self.side_a, self.side_b,
                    key=lambda value: value.get_big_z())
        front.convert_and_show(canvas)

    def get_big_x(self):
        return max(self.side_a.get_big_x(), self.side_b.get_big_x())

    def get_small_x(self):
        return min(self.side_a.get_small_x(), self.side_b.get_small_x())

    def get_big_y(self):
        return max(self.side_a.get_big_y(), self.side_b.get_big_y())

    def get_small_y(self):
        return min(self.side_a.get_small_y(), self.side_b.get_small_y())

    def get_big_z(self):
        return max(self.side_a.get_big_z(), self.side_b.get_big_z())

    def get_small_z(self):
        return min(self.side_a.get_small_z(), self.side_b.get_small_z())

    def get_middle(self):
        a1, b1, c1 = self.side_b.get_middle().get_points()
        a2, b2, c2 = self.side_a.get_middle().get_points()
        x = (a1 + a2) / 2
        y = (b1 + b2) / 2
        z = (c1 + c2) / 2
        return Point3D(x, y, z)

    def get_board_top(self):
        return self.__board_top

    def get_board_bottom(self):
        return self.__board_bottom
