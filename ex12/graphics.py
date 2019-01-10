from .matrix_3D import Matrix3D, Point3D
from .board import Board
from .shapes import Shapes
import random
import math
import copy


class Graphics:
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__canvas.configure(height=900, width=900, bg='grey')
        self.__canvas.master.bind('<Key>', self.__key_pressed)

        self.magoz = (900 / 2, 900 / 3, 700)
        self.light_source = (500, 0, -500)

        orange = self.__canvas.winfo_rgb('orange')

        # TODO: Decide whether shapes have their own classes.
        self.table = Shapes(self.magoz, self.light_source,
                            'ex12/table.obj', orange,
                            'item1')

        navy = self.__canvas.winfo_rgb('blue4')
        self.__board = Board(self.magoz, self.light_source, navy)
        self.coin_temp = Shapes(self.magoz, self.light_source, "ex12/coin.obj",
                                "", 'item2')

        self.__cur_state = Matrix3D()
        self.__cur_state.setIdentity()

        self.__center_location = Point3D(0, 0, 100)

        self.__board.build_shape(self.__center_location.x,
                                 self.__center_location.y,
                                 self.__center_location.z + 200)
        self.table.build_shape(self.__center_location.x,
                               self.__board.get_big_y() + 700,
                               self.__center_location.z)

        self.__coins = [[]]
        self.__active_coins = []
        self.__column_points = [[]]

        # TODO: Move this stuff into board.
        self.__board_top = Point3D(self.__board.get_middle().x,
                                   self.__board.get_small_y(),
                                   self.__board.get_middle().z)
        self.__board_bottom = Point3D(self.__board.get_middle().x,
                                      self.__board.get_big_y(),
                                      self.__board.get_middle().z)

        self.__create_coins_and_column_pointers()
        self.__working = False
        self.prepare_and_draw_all()

    def prepare_and_draw_all(self):
        self.table.mull_points(self.__cur_state)
        self.__board.mull_points(self.__cur_state)
        self.coin_temp.mull_points(self.__cur_state)
        self.__center_location.mull_point(self.__cur_state)
        self.__board_top.mull_point(self.__cur_state)
        self.__board_bottom.mull_point(self.__cur_state)
        for column in self.__coins:
            for coin in column:
                coin.mull_points(self.__cur_state)
                coin.real_to_guf()
        for coin in self.__active_coins:
            coin.mull_points(self.__cur_state)
            coin.real_to_guf()
        for column in self.__column_points:
            for point in column:
                point.mull_point(self.__cur_state)
        self.table.real_to_guf()
        self.__board.real_to_guf()

        # TODO: Make this a sorted data structure:
        if self.__board_top.z < self.table.get_middle().z:
            self.table.convert_and_show(self.__canvas)
            self.__board.convert_and_show_back(self.__canvas)
            for coin in self.__active_coins:
                coin.convert_and_show(self.__canvas)
            self.__board.convert_and_show_front(self.__canvas)
        else:
            self.__board.convert_and_show_back(self.__canvas)
            for coin in self.__active_coins:
                coin.convert_and_show(self.__canvas)
            self.__board.convert_and_show_front(self.__canvas)
            self.table.convert_and_show(self.__canvas)
        self.__canvas.update_idletasks()

    def play_coin(self, column, color):
        coin_to_play = self.__coins[column].pop()
        color_rgb = self.__canvas.winfo_rgb(color)
        coin_to_play.set_color(color_rgb)
        self.__active_coins.append(coin_to_play)
        self.__place_coin(coin_to_play, column)

    def __place_coin(self, coin, column):
        point = self.__column_points[column].pop()
        dx, dy, dz = -coin.get_middle().x + point.x, -coin.get_middle().y + point.y, -coin.get_middle().z + point.z
        self.__animate_coin(point, coin, dx, dy, dz)

    def __animate_coin(self, point, coin, dx, dy, dz):

        matrix = Matrix3D()
        # matrix.setMatMove(dx, dy, dz)
        # coin.mull_points(matrix)
        # self.__cur_state.setIdentity()
        # self.prepare_and_draw_all()
        vx0 = 0
        vy0 = 0
        vz0 = 0
        ax = (2 * (dx - vx0) / (5 ** 2))
        ay = (2 * (dy - vy0) / (5 ** 2))
        az = (2 * (dz - vz0) / (5 ** 2))
        x0 = 0
        y0 = 0
        z0 = 0
        for i in range(1, 6):
            ddx = vx0 + 0.5 * ax * i **2
            ddy = vy0 + 0.5 * ay * i **2
            ddz = vy0 + 0.5 * az * i **2
            matrix.setMatMove(ddx - x0, ddy - y0, ddz - z0)
            x0 = ddx
            y0 = ddy
            z0 = ddz
            coin.mull_points(matrix)
            self.__cur_state.setIdentity()
            self.prepare_and_draw_all()

    def __create_coins_and_column_pointers(self):
        for i in range(7):
            self.__coins.append([])
            self.__column_points.append([])
            for j in range(6):
                point = Point3D(self.__board_top.x - 170 + 56 * i,
                                self.__board_top.y + 40 + 48 * j,
                                self.__board.get_middle().z)
                self.__column_points[i].append(point)

                new_coin = Shapes(self.magoz, self.light_source,
                                  "ex12/coin.obj", (0, 0, 0),
                                  'item%s%s' % (i, j))
                self.__coins[i].append(new_coin)
                new_coin.build_shape(self.__board_top.x - 170 + 56 * i,
                                     self.__board_top.y,
                                     self.__board.get_middle().z)

    def __key_pressed(self, event):



        key = event.keysym
        mat1 = Matrix3D()
        mat1.setIdentity()

        if key == 'plus':
            mat1.setMatMove(0, 0, -30)

        elif key == 'minus':
            mat1.setMatMove(0, 0, 30)

        elif key == 'Up':
            angle = math.pi / 45
            mat1.setMatRotateXFix(angle, *self.__center_location.get_points())

        elif key == 'Down':
            angle = -math.pi / 45
            mat1.setMatRotateXFix(angle, *self.__center_location.get_points())

        elif key == 'Left':
            angle = -math.pi / 45
            mat1.setMatRotateAxis(*self.__board_top.get_points(),
                                  *self.__board_bottom.get_points(), angle)

        elif key == 'Right':
            angle = math.pi / 45
            mat1.setMatRotateAxis(*self.__board_top.get_points(),
                                  *self.__board_bottom.get_points(), angle)

        elif key.isnumeric():
            try:
                self.play_coin(int(key), 'red')
                self.__cur_state.setIdentity()
            except IndexError:
                pass
            finally:
                return

        self.__cur_state = mat1
        self.prepare_and_draw_all()
