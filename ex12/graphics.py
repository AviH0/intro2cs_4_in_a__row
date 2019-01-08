from .matrix_3D import Matrix3D, Point3D
from .board import Board
from .shapes import Shapes
import math


class Graphics:
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__canvas.configure(height=900, width=900, bg='grey')
        self.__canvas.master.bind('<Key>', self.__key_pressed)
        self.magoz = (900 / 2, 900 / 3, 700)
        self.light_source = (500, 0, -500)
        self.table = Shapes(self.magoz, self.light_source,
                            'ex12/table.obj', "orange")
        self.__board = Board(self.magoz, self.light_source)
        self.__cur_state = Matrix3D()
        self.__cur_state.setIdentity()
        self.__camera_location = Point3D(0, 0, -50)
        self.__board_location = Point3D(0, 0, 100)
        self.__board.build_shape(*self.__board_location.get_points())
        self.table.build_shape(self.__board_location.x,
                               self.__board.get_big_y()+700,
                               self.__board_location.z )
        self.__board_top = Point3D(self.__board.get_middle().x,
                                   self.__board.get_small_y(),
                                   self.__board.get_middle().z)
        self.__board_bottom = Point3D(self.__board.get_middle().x,
                                      self.__board.get_big_y(),
                                      self.__board.get_middle().z)
        self.prepare_and_draw_all()

    def prepare_and_draw_all(self):
        self.table.mull_points(self.__cur_state)
        self.__board.mull_points(self.__cur_state)
        self.__board_location.mull_point(self.__cur_state)
        self.__board_top.mull_point(self.__cur_state)
        self.__board_bottom.mull_point(self.__cur_state)
        self.table.real_to_guf()
        self.__board.real_to_guf()

        if self.__board_top.z < self.table.get_middle().z:
            self.table.convert_and_show(self.__canvas)
            self.__board.convert_and_show(self.__canvas)
        else:
            self.__board.convert_and_show(self.__canvas)
            self.table.convert_and_show(self.__canvas)

    def __save_coords(self, event):
        self.__mouse_start = (event.x, event.y)

    def __key_pressed(self, event):

        key = event.keysym
        mat1 = Matrix3D()
        mat1.setIdentity()

        if key == 'Up':
            angle = math.pi / 90
            mat1.setMatRotateXFix(angle, *self.__board_location.get_points())

        elif key == 'Down':
            angle = -math.pi / 90
            mat1.setMatRotateXFix(angle, *self.__board_location.get_points())

        elif key == 'Left':
            angle = -math.pi / 90
            mat1.setMatRotateAxis(*self.__board_top.get_points(),
                                  *self.__board_bottom.get_points(), angle)

        elif key == 'Right':
            angle = math.pi / 90
            mat1.setMatRotateAxis(*self.__board_top.get_points(),
                                  *self.__board_bottom.get_points(), angle)

        self.__cur_state = mat1
        self.prepare_and_draw_all()
