import numpy as np
from .matrix_3D import Point3D


class Shapes:
    def __init__(self, magoz, light_source, filename, color, id):
        self.__magoz = magoz
        self.light_source = light_source
        self.__color = color
        self.light_source = self.light_source.get_points() / np.linalg.norm(
            self.light_source.get_points())
        self.filename = filename
        self.__needs_update = True
        self.__id = id
        self.__num_vertices = 0
        self.__num_faces = 0
        self.x_real = []  # [0 for i in range(num_vertices * 2)]
        self.y_real = []  # [0 for i in range(num_vertices * 2)]
        self.z_real = []  # [0 for i in range(num_vertices * 2)]

        self.__guf_order = []
        self.x_guf = []  # [[0 for i in range(num_vertices)] for j in
        # range(num_facets)]
        self.y_guf = []  # [[0 for i in range(num_vertices)] for j in
        # range(num_facets)]
        self.z_guf = []  # [[0 for i in range(num_vertices)] for j in
        # range(num_facets)]
        self.__colors = []
        self.__shades = []
        self.__disp = []

        self.__vertices = []
        self.__faces = []

    def build_shape(self, x, y, z):
        self.__build_from_file()
        for vertice in self.__vertices:
            xv, yv, zv = vertice.split(' ')
            self.x_real.append(float(xv) + x)
            self.y_real.append(float(yv) + y)
            self.z_real.append(float(zv) + z)
        self.__guf_order = [i for i in range(len(self.__faces))]
        # self.real_to_guf()
        # self.__build_normals()

    def real_to_guf(self):
        if not self.__needs_update:
            return
        self.x_guf = []
        self.y_guf = []
        self.z_guf = []
        self.__colors = []
        red, green, blue = self.__color
        for face in self.__faces:
            a, b, c = face.split(' ')
            a = int(a)
            b = int(b)
            c = int(c)
            x = [self.x_real[a - 1], self.x_real[b - 1],
                 self.x_real[c - 1]]
            y = [self.y_real[a - 1], self.y_real[b - 1],
                 self.y_real[c - 1]]
            z = [self.z_real[a - 1], self.z_real[b - 1],
                 self.z_real[c - 1]]

            self.x_guf.append(x)
            self.y_guf.append(y)
            self.z_guf.append(z)
            n = np.cross((x[0], y[0], z[0]), (x[1], y[1], z[1]))
            n = n / np.linalg.norm(n)
            shade = np.dot((n[0], n[1], n[2]), self.light_source)
            LIGHT_SOURCE_STRENGTH = 0.2
            self.__colors.append(
                "#%04x%04x%04x" % (int(red - 0.5 * abs(shade) * red),
                                   int(green - 0.5 * abs(shade) * green),
                                   int(blue - 0.5 * abs(shade) * blue)))

        self.__guf_order.sort(key=lambda value: min(self.z_guf[value]),
                              reverse=True)
        self.__disp = []
        for i in range(len(self.__faces)):
            self.__convert(self.x_guf[self.__guf_order[i]],
                           self.y_guf[self.__guf_order[i]],
                           self.z_guf[self.__guf_order[i]])

    # self.guf_order = [i for i in range(self.__num_faces)]

    def __check(self, x1, y1, x2, y2, x3, y3):
        return x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2) > 0

    def __convert(self, x, y, z):
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
        for i in range(len(self.x_guf)):
            self.__convert(self.x_guf, self.y_guf, self.z_guf)

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
            z = self.z_real
        return max(z)

    def get_small_z(self):
        return min(self.z_real)

    def get_big_y(self, y=None):
        if not y:
            y = self.y_real
        return max(y)

    def get_small_y(self):
        return min(self.y_real)

    def get_big_x(self, x=None):
        if not x:
            x = self.x_real
        return max(x)

    def get_small_x(self):
        return min(self.x_real)

    def get_middle(self):
        x = (self.get_big_x() + self.get_small_x()) / 2
        y = (self.get_big_y() + self.get_small_y()) / 2
        z = (self.get_big_z() + self.get_small_z()) / 2
        return Point3D(x, y, z)

    def convert_and_show(self, canvas):

        tag = self.__id
        if not self.__needs_update:
            canvas.tag_raise(tag)
            return

        canvas.delete(tag)

        for i in range(self.__num_faces):

            # TODO: Tidy
            if not self.__check(*self.__disp[self.__guf_order[i]][0],
                                *self.__disp[self.__guf_order[i]][1],
                                *self.__disp[self.__guf_order[i]][2]):
                color = self.__colors[self.__guf_order[i]]
                canvas.create_polygon(self.__disp[self.__guf_order[i]],
                                      fill=color, tag=tag)
        self.__needs_update = False

    def mull_points(self, matrix):
        if matrix.check_identity():
            return
        self.x_real, self.y_real, self.z_real = matrix.mullAllPoints(
            self.x_real,
            self.y_real,
            self.z_real,
            self.__num_vertices)
        self.__needs_update = True

    def set_color(self, color):
        self.__color = color
