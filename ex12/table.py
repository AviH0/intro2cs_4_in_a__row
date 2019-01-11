from .shapes import Shapes
from .matrix_3D import Point3D


class Table:

    def __init__(self, magoz, light_source, color):
        self.__table_top = Shapes(magoz, light_source, 'ex12/table_top.obj',
                                  color, 'Table_top')
        self.__table_legs = Shapes(magoz, light_source, 'ex12/table_legs.obj',
                                   color, 'Table_legs')
        self.__shape_list = [self.__table_top, self.__table_legs]

    def build_shape(self, x, y, z):
        self.__table_legs.build_shape(x, y, z)
        self.__table_top.build_shape(x, y, z)

    def mull_points(self, mat):
        self.__table_top.mull_points(mat)
        self.__table_legs.mull_points(mat)

    def real_to_guf(self):
        self.__table_legs.real_to_guf()
        self.__table_top.real_to_guf()

    def get_middle(self):
        a1, b1, c1 = self.__table_top.get_middle().get_points()
        a2, b2, c2 = self.__table_legs.get_middle().get_points()
        x = (a1 + a2) / 2
        y = (b1 + b2) / 2
        z = (c1 + c2) / 2
        return Point3D(x, y, z)

    def convert_and_show(self, canvas):
        self.__shape_list.sort(key=lambda value: value.get_middle().z, reverse=True)
        for shape in self.__shape_list:
            shape.convert_and_show(canvas)
