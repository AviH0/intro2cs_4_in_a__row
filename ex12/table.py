from .shapes import Shapes
from .matrix_3D import Point3D
import os

class Table:
    """
    A class for displaying a 3D table.
    """
    # Files:
    PATH = os.path.dirname(os.path.realpath(__file__))
    TOP_FILE = PATH + '/table_top.obj'
    LEGS_FILE = PATH + '/table_legs.obj'

    # Tags:
    TOP_TAG = 'Table_top'
    LEGS_TAG = 'Table_legs'

    def __init__(self, magoz, light_source, color):
        """
        Create an instance of the class table
        :param magoz: A Point3D object with the perspective location.
        :param light_source:A Point3D object with the light-source location.
        :param color: rgb values for this object's color
        """
        self.__table_top = Shapes(magoz, light_source, self.TOP_FILE,
                                  color, self.TOP_TAG)
        self.__table_legs = Shapes(magoz, light_source, self.LEGS_FILE,
                                   color, self.LEGS_TAG)
        self.__shape_list = [self.__table_top, self.__table_legs]

    def build_shape(self, x, y, z):
        """
        Build the shape in the given coordinates.
        :param x: The x coordinate to build in.
        :param y: The y coordinate to build in.
        :param z: The z ooordinate to build in.
        """
        self.__table_legs.build_shape(x, y, z)
        self.__table_top.build_shape(x, y, z)

    def mull_points(self, mat):
        """
        Multiply the shapes vertices by a matrix.
        :param matrix: A Matrix_3D object to mulltiply by.
        """
        self.__table_top.mull_points(mat)
        self.__table_legs.mull_points(mat)

    def real_to_guf(self):
        """
        Update the faces lists from the vertices lists
        """
        self.__table_legs.real_to_guf()
        self.__table_top.real_to_guf()

    def get_middle(self):
        """
        Get the coordinates of the middle of the shape.
        :return: A Point3D object with the middle of the shape.
        """
        a1, b1, c1 = self.__table_top.get_middle().get_points()
        a2, b2, c2 = self.__table_legs.get_middle().get_points()
        x = (a1 + a2) / 2
        y = (b1 + b2) / 2
        z = (c1 + c2) / 2
        return Point3D(x, y, z)

    def get_big_z(self):
        """
        Get the biggest z coordinate of the shape.
        """
        return max(self.__table_legs.get_big_z(), self.__table_top.get_big_z())

    def draw(self, canvas):
        """
        Draw the table
        :param canvas: A tkinter canvas to work on.
        :return:
        """
        self.__shape_list.sort(key=lambda value: value.get_middle().z,
                               reverse=True)
        for shape in self.__shape_list:
            shape.draw(canvas)
