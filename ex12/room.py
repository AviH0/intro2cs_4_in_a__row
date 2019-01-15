from .shapes import Shapes
import os

class Room:
    """
    A class for displaying a 3D table.
    """

    NUM_WALLS = 4

    # FILES:
    PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
    WALL_FILE = PATH + '/wall%s.obj'
    CEILING_FILE = PATH + '/ceiling.obj'

    # Tags:
    WALL_TAG = 'wall%s'
    CEILING_TAG = 'ceiling'

    def __init__(self, magoz, light_source, color):
        """
        Create an instance of the class table
        :param magoz: A Point3D object with the perspective location.
        :param light_source:A Point3D object with the light-source location.
        :param color: rgb values for this object's color
        """
        self.__walls = []
        self.__ceiling = Shapes(magoz, light_source, self.CEILING_FILE, color,
                                self.CEILING_TAG)
        self.create_room(magoz, light_source, color)

    def create_room(self, magoz, light_source, color):
        """
        Create the walls and ceiling in the positions.
       :param magoz: A Point3D object with the perspective location.
        :param light_source:A Point3D object with the light-source location.
        :param color: rgb values for this object's color
        :return:
        """
        for i in range(1, self.NUM_WALLS + 1):
            wall = Shapes(magoz, light_source, self.WALL_FILE % i, color,
                          self.WALL_TAG % i)
            self.__walls.append(wall)

    def build_shape(self, x, y, z):
        """
        Build the shape in the given coordinates.
        :param x: The x coordinate to build in.
        :param y: The y coordinate to build in.
        :param z: The z ooordinate to build in.
        """
        self.__ceiling.build_shape(x, y, z)
        for wall in self.__walls:
            wall.build_shape(x, y, z)

    def real_to_guf(self):
        """
        Update the faces lists from the vertices lists
        """
        self.__ceiling.real_to_guf()
        for wall in self.__walls:
            wall.real_to_guf()

    def mull_points(self, mat):
        """
        Multiply the shapes vertices by a matrix.
        :param matrix: A Matrix_3D object to mulltiply by.
        """
        self.__ceiling.mull_points(mat)
        for wall in self.__walls:
            wall.mull_points(mat)

    def draw(self, canvas, camera_z):
        """
        Draw the room.
        :param canvas: A tkinter canvas to work on.
        :return:
        """
        for wall in self.__walls:
            if wall.get_middle().z > camera_z:
                wall.draw(canvas)
            else:
                wall.remove(canvas)
        self.__ceiling.draw(canvas)

    def get_middle(self):
        """
        Get the coordinates of the middle of the shape.
        :return: A Point3D object with the middle of the shape.
        """
        return self.__ceiling.get_middle()
