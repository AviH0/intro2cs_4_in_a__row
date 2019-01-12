from .shapes import Shapes
from .matrix_3D import Point3D


class Room:
    NUM_WALLS = 4

    def __init__(self, magoz, light_source, color):
        self.__walls = []
        self.__ceiling = Shapes(magoz, light_source, 'ex12/ceiling.obj', color,
                                'ceiling')
        self.create_room(magoz, light_source, color)

    def create_room(self, magoz, light_source, color):
        for i in range(1, self.NUM_WALLS + 1):
            wall = Shapes(magoz, light_source, 'ex12/wall%s.obj' % i, color,
                          'wall%s' % i)
            self.__walls.append(wall)

    def build_shape(self, x, y, z):
        self.__ceiling.build_shape(x, y, z)
        for wall in self.__walls:
            wall.build_shape(x, y, z)

    def real_to_guf(self):
        self.__ceiling.real_to_guf()
        for wall in self.__walls:
            wall.real_to_guf()

    def mull_points(self, mat):
        self.__ceiling.mull_points(mat)
        for wall in self.__walls:
            wall.mull_points(mat)


    def convert_and_show(self, canvas, camera_z):
        for wall in self.__walls:
            if wall.get_middle().z > camera_z:
                wall.convert_and_show(canvas)
        self.__ceiling.convert_and_show(canvas)
