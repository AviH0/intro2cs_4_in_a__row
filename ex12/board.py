from .shapes import Shapes
from .matrix_3D import Point3D
import os


class Board:
    """
    A class for displaying a 3D Connect-four board.
    """

    # Files:
    PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
    SIDE_A_FILE = PATH + '/SideA.obj'
    SIDE_B_FILE = PATH + '/SideB.obj'

    # Tags:
    SIDE_A_TAG = 'boardA'
    SIDE_B_TAG = 'boardB'

    def __init__(self, magoz, light_source, color):
        """
        Create an instance of the class Board
        :param magoz: A Point3D object with the perspective location.
        :param light_source:A Point3D object with the light-source location.
        :param color: rgb values for this object's color
        """
        self.side_a = Shapes(magoz, light_source, self.SIDE_A_FILE, color,
                             self.SIDE_A_TAG)
        self.side_b = Shapes(magoz, light_source, self.SIDE_B_FILE, color,
                             self.SIDE_B_TAG)
        self.__board_top = None
        self.__board_bottom = None

    def build_shape(self, x, y, z):
        """
        Build the shape in the given coordinates.
        :param x: The x coordinate to build in.
        :param y: The y coordinate to build in.
        :param z: The z ooordinate to build in.
        """
        self.side_a.build_shape(x, y, z)
        self.side_b.build_shape(x, y, z)
        self.__board_top = Point3D(self.get_middle().x,
                                   self.get_small_y(),
                                   self.get_middle().z)
        self.__board_bottom = Point3D(self.get_middle().x,
                                      self.get_big_y(),
                                      self.get_middle().z)

    def real_to_guf(self):
        """
        Update the faces lists from the vertices lists
        """
        self.side_a.real_to_guf()
        self.side_b.real_to_guf()

    def mull_points(self, mat):
        """
        Multiply the shapes vertices by a matrix.
        :param matrix: A Matrix_3D object to mulltiply by.
        """
        self.side_a.mull_points(mat)
        self.side_b.mull_points(mat)
        self.__board_top.mull_point(mat)
        self.__board_bottom.mull_point(mat)

    def draw_back(self, canvas):
        """
        Draw the back half of the board.
        :param canvas: A Tkinter Canvas to work on.
        """
        back = max(self.side_a, self.side_b,
                   key=lambda value: value.get_big_z())
        back.draw(canvas)

    def draw_front(self, canvas):
        """
        Draw the back half of the board.
        :param canvas: A Tkinter Canvas to work on.
        """
        front = min(self.side_a, self.side_b,
                    key=lambda value: value.get_big_z())
        front.draw(canvas)

    def get_big_x(self):
        """
        Get the biggest x coordinate of the shape.
        """
        return max(self.side_a.get_big_x(), self.side_b.get_big_x())

    def get_small_x(self):
        """
        Get the smallest x coordinate of the shape.
        """
        return min(self.side_a.get_small_x(), self.side_b.get_small_x())

    def get_big_y(self):
        """
        Get the biggest y coordinate of the shape.
        """
        return max(self.side_a.get_big_y(), self.side_b.get_big_y())

    def get_small_y(self):
        """
        Get the smallest y coordinate of the shape.
        """
        return min(self.side_a.get_small_y(), self.side_b.get_small_y())

    def get_big_z(self):
        """
        Get the biggest z coordinate of the shape.
        """
        return max(self.side_a.get_big_z(), self.side_b.get_big_z())

    def get_small_z(self):
        """
        Get the smallest z coordinate of the shape.
        """
        return min(self.side_a.get_small_z(), self.side_b.get_small_z())

    def get_middle(self):
        """
        Get the coordinates of the middle of the shape.
        :return: A Point3D object with the middle of the shape.
        """
        a1, b1, c1 = self.side_b.get_middle().get_points()
        a2, b2, c2 = self.side_a.get_middle().get_points()
        x = (a1 + a2) / 2
        y = (b1 + b2) / 2
        z = (c1 + c2) / 2
        return Point3D(x, y, z)

    def get_board_top(self):
        """
        get the pointer to the top of the board.
        """
        return self.__board_top

    def get_board_bottom(self):
        """
        get the pointer to the bottom of the board.
        """
        return self.__board_bottom
