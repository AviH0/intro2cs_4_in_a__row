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
        Convert the values for a face into 2-d coords for display.
        :param x: The face's x coords.
        :param y: The face's y coords.
        :param z: The face's z coords.
        """
        # If the perspective point is set, use it to convert:
        if self.__magoz:
            lst = []
            for i in range(3):
                d = self.__magoz.z / (self.__magoz.z + z[i])
                lst.append(
                    [x[i] * d + self.__magoz.x, y[i] * d + self.__magoz.y])
            self.__disp.append(lst)
        else:  # There is not perspective point, use direct projection.
            for i in range(3):
                self.__disp.append((x[i], y[i]))

    def __build_from_file(self):
        """
        Build the faces and vertices lists from the obj file
        """
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
                return False

    def get_big_z(self, z=None):
        """
        Get the biggest z coordinate of the shape.
        :param z: A partial list of z coordinates.
        """
        if not z:
            z = self.z_vertices
        return max(z)

    def get_small_z(self):
        """
        Get the smallest z coordinate of the shape.
        """
        return min(self.z_vertices)

    def get_big_y(self, y=None):
        """
        Get the biggest y coordinate of the shape.
        :param y: A partial list of y coordinates.
        """
        if not y:
            y = self.y_vertices
        return max(y)

    def get_small_y(self):
        """
        Get the smallest y coordinate of the shape.
        """
        return min(self.y_vertices)

    def get_big_x(self, x=None):
        """
        Get the biggest x coordinate of the shape.
        :param x: A partial list of x coordinates.
        """
        if not x:
            x = self.x_vertices
        return max(x)

    def get_small_x(self):
        """
        Get the smallest x coordinate of the shape.
        """
        return min(self.x_vertices)

    def get_middle(self):
        """
        Get the coordinates of the middle of the shape.
        :return: A Point3D object with the middle of the shape.
        """
        x = (self.get_big_x() + self.get_small_x()) / 2
        y = (self.get_big_y() + self.get_small_y()) / 2
        z = (self.get_big_z() + self.get_small_z()) / 2
        return Point3D(x, y, z)

    def remove(self, canvas):
        """
        Remove the shape from the canvas.
        :param canvas: A Tkinter Canvas object to work on.
        """
        canvas.delete(self.__tag)

    def draw(self, canvas):
        """
        Draw the shape on a canvas.
        :param canvas: A Tkinter Canvas object to work on.
        """

        tag = self.__tag
        # If there is not need to update, just raise the shape so it is at the
        # top of the stack:
        if not self.__needs_update:
            canvas.tag_raise(tag)
            return

        # Remove the previously drawn shape:
        canvas.delete(tag)

        # For each face, check if it facing towards the camera. If so, draw it.
        # Iterate according to the correct order:
        for i in range(self.__num_faces):
            if not self.__check(*self.__disp[self.__faces_order[i]][0],
                                *self.__disp[self.__faces_order[i]][1],
                                *self.__disp[self.__faces_order[i]][2]):
                color = self.__colors[self.__faces_order[i]]
                canvas.create_polygon(self.__disp[self.__faces_order[i]],
                                      fill=color, tag=tag)

        # Set the update flag to false:
        self.__needs_update = False

    def mull_points(self, matrix):
        """
        Multiply the shapes vertices by a matrix.
        :param matrix: A Matrix_3D object to mulltiply by.
        """

        # If the matrix is the identity, skip:
        if matrix.check_identity():
            return

        # Multiply and set the flag to update:
        self.x_vertices, self.y_vertices, self.z_vertices = matrix.mullAllPoints(
            self.x_vertices,
            self.y_vertices,
            self.z_vertices,
            self.__num_vertices)
        self.__needs_update = True

    def set_color(self, color):
        """
        Set the color to a specific value.
        :param color: A tuple of RGB color values.
        """
        self.__color = color
