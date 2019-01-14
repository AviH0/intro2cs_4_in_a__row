import numpy as np
from .matrix_3D import Point3D


class Shapes:

    LIGHT_SOURCE_PERCENTAGE = 0.2

    def __init__(self, magoz, light_source, filename, color, tag):
        """
        Create an instance of the class shape.
        :param magoz: A Point3D object with the perspective location.
        :param light_source:A Point3D object with the light-source location.
        :param filename: A string with the past to an .OBJ file with a 3D
                         object.
        :param color: rgb values for this object's color
        :param tag: A String with this object's unique tag.
        """
        self.__magoz = magoz
        self.light_source = light_source
        self.__color = color
        self.light_source = self.light_source.get_points() / np.linalg.norm(
            self.light_source.get_points())
        self.filename = filename
        self.__tag = tag

        # Set the flag to update positions:
        self.__needs_update = True


        # Initiate all the needed lists as empty:
        self.__num_vertices = 0
        self.__num_faces = 0
        self.x_vertices = []
        self.y_vertices = []
        self.z_vertices = []
        self.__faces_order = []
        self.x_face = []
        self.y_face = []
        self.z_face = []
        self.__colors = []
        self.__shades = []
        self.__disp = []
        self.__vertices = []
        self.__faces = []

    def build_shape(self, x, y, z):
        """
        Build the shape in the given coordinates.
        :param x: The x coordinate to build in.
        :param y: The y coordinate to build in.
        :param z: The z oordinate to build in.
        """

        # Build the vertex and and faces list from the file:
        self.__build_from_file()
        for vertex in self.__vertices:
            xv, yv, zv = vertex.split(' ')
            self.x_vertices.append(float(xv) + x)
            self.y_vertices.append(float(yv) + y)
            self.z_vertices.append(float(zv) + z)
        self.__faces_order = [i for i in range(len(self.__faces))]

    def real_to_guf(self):
        """
        Update the faces lists from the vertices lists
        """

        # If there is nothing to update, return
        if not self.__needs_update:
            return

        # Empty the lists and refill them:
        self.x_face = []
        self.y_face = []
        self.z_face = []
        self.__colors = []
        red, green, blue = self.__color
        for face in self.__faces:
            a, b, c = face.split(' ')
            a = int(a)
            b = int(b)
            c = int(c)
            x = [self.x_vertices[a - 1], self.x_vertices[b - 1],
                 self.x_vertices[c - 1]]
            y = [self.y_vertices[a - 1], self.y_vertices[b - 1],
                 self.y_vertices[c - 1]]
            z = [self.z_vertices[a - 1], self.z_vertices[b - 1],
                 self.z_vertices[c - 1]]

            # Add the current face to the lists:
            self.x_face.append(x)
            self.y_face.append(y)
            self.z_face.append(z)

            # Calculate this face's normal:
            n = np.cross((x[0], y[0], z[0]), (x[1], y[1], z[1]))
            n = n / np.linalg.norm(n)
            # Calculate the shading factor for this face:
            shade = np.dot((n[0], n[1], n[2]), self.light_source)
            # Calculate the RGB values for this face's color and add them to
            # the list:
            factor = self.LIGHT_SOURCE_PERCENTAGE
            self.__colors.append(
                "#%04x%04x%04x" % (int(red - factor * abs(shade) * red),
                                   int(green - factor * abs(shade) * green),
                                   int(blue - factor * abs(shade) * blue)))

        # Set the order of display for all the faces:
        self.__faces_order.sort(key=lambda value: min(self.z_face[value]),
                                reverse=True)
        self.__disp = []
        for i in range(len(self.__faces)):
            self.__convert(self.x_face[self.__faces_order[i]],
                           self.y_face[self.__faces_order[i]],
                           self.z_face[self.__faces_order[i]])

    def __check(self, x1, y1, x2, y2, x3, y3):
        """
        Check if a face is facing towards the camera or not.
        """

        return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2) > 0

    def __convert(self, x, y, z):
        """

        :param x:
        :param y:
        :param z:
        :return:
        """
        if self.__magoz:
            lst = []
            for i in range(3):
                d = self.__magoz.z / (self.__magoz.z + z[i])
                lst.append(
                    [x[i] * d + self.__magoz.x, y[i] * d + self.__magoz.y])
            self.__disp.append(lst)
        else:
            for i in range(3):
                self.__disp.append((x[i], y[i]))

    def convert_now(self):
        for i in range(len(self.x_face)):
            self.__convert(self.x_face, self.y_face, self.z_face)

    def __build_from_file(self):
        self.__num_vertices = 0
        self.__num_faces = 0
        with open(self.filename, 'r') as f:
            try:
                f_str = f.read().split('\n')
                for line in f_str:
                    if line:
                        if line[0] == "v":
                            self.__vertices.append(line[2:])
                            self.__num_vertices += 1
                        elif line[0] == 'f':
                            self.__faces.append(line[2:])
                            self.__num_faces += 1
            except IOError:
                print("error!")

    def get_big_z(self, z=None):
        if not z:
            z = self.z_vertices
        return max(z)

    def get_small_z(self):
        return min(self.z_vertices)

    def get_big_y(self, y=None):
        if not y:
            y = self.y_vertices
        return max(y)

    def get_small_y(self):
        return min(self.y_vertices)

    def get_big_x(self, x=None):
        if not x:
            x = self.x_vertices
        return max(x)

    def get_small_x(self):
        return min(self.x_vertices)

    def get_middle(self):
        x = (self.get_big_x() + self.get_small_x()) / 2
        y = (self.get_big_y() + self.get_small_y()) / 2
        z = (self.get_big_z() + self.get_small_z()) / 2
        return Point3D(x, y, z)

    def remove(self, canvas):
        canvas.delete(self.__tag)

    def convert_and_show(self, canvas):

        tag = self.__tag
        if not self.__needs_update:
            canvas.tag_raise(tag)
            return

        canvas.delete(tag)

        for i in range(self.__num_faces):

            # TODO: Tidy
            if not self.__check(*self.__disp[self.__faces_order[i]][0],
                                *self.__disp[self.__faces_order[i]][1],
                                *self.__disp[self.__faces_order[i]][2]):
                color = self.__colors[self.__faces_order[i]]
                canvas.create_polygon(self.__disp[self.__faces_order[i]],
                                      fill=color, tag=tag)
        self.__needs_update = False

    def mull_points(self, matrix):
        if matrix.check_identity():
            return
        self.x_vertices, self.y_vertices, self.z_vertices = matrix.mullAllPoints(
            self.x_vertices,
            self.y_vertices,
            self.z_vertices,
            self.__num_vertices)
        self.__needs_update = True

    def set_color(self, color):
        self.__color = color
