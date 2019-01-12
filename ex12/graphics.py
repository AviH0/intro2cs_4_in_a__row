from .matrix_3D import Matrix3D, Point3D
from .board import Board
from .shapes import Shapes
from .table import Table
from .room import Room
import math


class Graphics:
    def __init__(self, canvas, player_1_color='red', player_2_color='green'):
        self.__canvas = canvas
        self.__canvas.configure(height=900, width=900, bg='grey')
        self.__canvas.master.bind('<Key>', self.__key_pressed)

        self.magoz = (900 / 2, 900 / 3, 5000)
        self.light_source = (500, 500, 4900)
        room_light_source = (500, 0, 5000)
        self.__center_location = Point3D(0, 0, 5000)

        orange = self.__canvas.winfo_rgb('darkorange4')
        navy = self.__canvas.winfo_rgb('blue4')
        wall_color = self.__canvas.winfo_rgb('aquamarine4')
        floor_color = self.__canvas.winfo_rgb('grey10')
        black = self.__canvas.winfo_rgb('black')
        self.__player_1_color = self.__canvas.winfo_rgb(player_1_color)
        self.__player_2_color = self.__canvas.winfo_rgb(player_2_color)

        # TODO: Decide whether shapes have their own classes.
        self.table = Table(self.magoz, self.light_source, orange)
        self.__floor = Shapes(self.magoz, room_light_source, 'ex12/floor.obj',
                              floor_color, 'floor')
        self.__room = Room(self.magoz, room_light_source, wall_color)
        self.__text = Shapes(self.magoz, room_light_source, 'ex12/text.obj',
                             black, 'text')
        self.__board = Board(self.magoz, self.light_source, navy)
        self.__player = Shapes(self.magoz, self.light_source,
                               'ex12/player.obj', navy,
                               'player')
        self.__player_1 = Shapes(self.magoz, self.light_source,
                                 'ex12/number_1.obj', self.__player_1_color,
                                 'player_number')
        self.__player_2 = Shapes(self.magoz, self.light_source,
                                 'ex12/number_2.obj', self.__player_2_color,
                                 'player_number')

        self.__players = [self.__player_1, self.__player_2]
        self.__player_colors = [self.__player_1_color, self.__player_2_color]

        self.__current_player = 0

        self.__cur_state = Matrix3D()

        self.__cur_state.setMatScale(*self.__center_location.get_points(), 1.5,
                                     1.5, 1.5)

        self.__board.build_shape(self.__center_location.x,
                                 self.__center_location.y,
                                 self.__center_location.z + 200)
        self.table.build_shape(self.__center_location.x,
                               self.__board.get_big_y() + 700,
                               self.__center_location.z)
        self.__room.build_shape(self.__center_location.x,
                                self.__board.get_big_y() + 700,
                                self.__center_location.z - 1000)
        self.__floor.build_shape(self.__center_location.x,
                                 self.__board.get_big_y() + 700,
                                 self.__center_location.z - 1000)
        self.__text.build_shape(self.__center_location.x,
                                self.__board.get_big_y() + 700,
                                self.__center_location.z - 1000)

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

        self.__player.build_shape(self.__board_top.x - 15,
                                  self.__board_top.y - 25,
                                  self.__board_top.z - 25)
        self.__player_1.build_shape(self.__board_top.x - 15,
                                    self.__board_top.y - 25,
                                    self.__board_top.z - 25)
        self.__player_2.build_shape(self.__board_top.x - 15,
                                    self.__board_top.y - 25,
                                    self.__board_top.z - 25)

        self.__create_coins_and_column_pointers()

        self.__time = 0
        self.__canvas.create_text(110, 50, text='TIME:', fill='black',
                                  font="Helvetica 30 bold", tags='time')



        self.prepare_and_draw_all()

        self.__update_clock()

    def prepare_and_draw_all(self):

        self.__text.mull_points(self.__cur_state)
        self.table.mull_points(self.__cur_state)
        self.__board.mull_points(self.__cur_state)
        self.__room.mull_points(self.__cur_state)
        self.__floor.mull_points(self.__cur_state)
        self.__center_location.mull_point(self.__cur_state)
        self.__board_top.mull_point(self.__cur_state)
        self.__board_bottom.mull_point(self.__cur_state)
        self.__player.mull_points(self.__cur_state)
        self.__player_1.mull_points(self.__cur_state)
        self.__player_2.mull_points(self.__cur_state)

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
        self.__text.real_to_guf()
        self.__room.real_to_guf()
        self.__floor.real_to_guf()
        self.table.real_to_guf()
        self.__board.real_to_guf()
        self.__player.real_to_guf()
        self.__player_1.real_to_guf()
        self.__player_2.real_to_guf()

        # TODO: Make this a sorted data structure:
        self.__room.convert_and_show(self.__canvas, self.__center_location.z)
        if self.__text.get_middle().z > self.__board.get_middle().z:
            self.__text.convert_and_show(self.__canvas)
        if self.__floor.get_middle().z > self.__board_top.z:
            self.__floor.convert_and_show(self.__canvas)
        if self.__board_top.z < self.table.get_middle().z:
            self.table.convert_and_show(self.__canvas)
            self.__board.convert_and_show_back(self.__canvas)
            for coin in self.__active_coins:
                coin.convert_and_show(self.__canvas)
            self.__board.convert_and_show_front(self.__canvas)
            self.__player.convert_and_show(self.__canvas)
            self.__players[self.__current_player].convert_and_show(
                self.__canvas)
        else:
            self.__board.convert_and_show_back(self.__canvas)
            for coin in self.__active_coins:
                coin.convert_and_show(self.__canvas)
            self.__board.convert_and_show_front(self.__canvas)
            self.__player.convert_and_show(self.__canvas)
            self.__players[self.__current_player].convert_and_show(
                self.__canvas)
            self.table.convert_and_show(self.__canvas)
        self.__canvas.tag_raise('time')
        # self.__canvas.update_idletasks()
        self.__cur_state.setIdentity()
        self.__canvas.master.after(200, self.prepare_and_draw_all)

    def play_coin(self, column):
        color = self.__player_colors[self.__current_player]
        coin_to_play = self.__coins[column].pop()
        coin_to_play.set_color(color)
        self.__active_coins.append(coin_to_play)
        self.__current_player ^= 1
        self.__place_coin(coin_to_play, column)

    def __place_coin(self, coin, column):
        point = self.__column_points[column].pop()
        dx, dy, dz = -coin.get_middle().x + point.x, -coin.get_middle().y + point.y, -coin.get_middle().z + point.z
        self.__animate_coin(point, coin, dx, dy, dz)

    def __animate_coin(self, point, coin, dx, dy, dz, x0=0, y0=0, z0=0, i=1):

        matrix = Matrix3D()
        # matrix.setMatMove(dx, dy, dz)
        # coin.mull_points(matrix)
        # self.__cur_state.setIdentity()
        # self.prepare_and_draw_all()
        ax = (2 * dx / (5 ** 2))
        ay = (2 * dy / (5 ** 2))
        az = (2 * dz / (5 ** 2))
        # x0 = 0
        # y0 = 0
        # z0 = 0
        # for i in range(1, 6):
        ddx = 0.5 * ax * i ** 2
        ddy = 0.5 * ay * i ** 2
        ddz = 0.5 * az * i ** 2
        matrix.setMatMove(ddx - x0, ddy - y0, ddz - z0)
        x0 = ddx
        y0 = ddy
        z0 = ddz
        coin.mull_points(matrix)
        self.__cur_state.setIdentity()
        if i < 5:
            self.__canvas.master.after(70,
                                       lambda: self.__animate_coin(self, coin,
                                                                   dx, dy, dz,
                                                                   x0, y0, z0,
                                                                   i + 1))
        # self.__canvas.update_idletasks()
        # self.prepare_and_draw_all()

    def calc_one_coin(self):
        coin = Shapes(self.magoz, self.light_source,
                      "ex12/coin.obj", (0, 0, 0),
                      '')
        mat = Matrix3D()
        mat.setMatMove(1, 1, 1)
        coin.mull_points(mat)

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

    def __update_clock(self):
        self.__time += 0.1
        self.__canvas.tag_raise('time')
        self.__canvas.itemconfig('time', text='TIME: ' + str(
            int(self.__time // 3600)) + ':' + str(
            int(self.__time // 60)) + ':' + str(int(self.__time % 60)))
        self.__canvas.update_idletasks()
        self.__canvas.master.after(100, self.__update_clock)

    def __key_pressed(self, event):

        key = event.keysym
        mat1 = Matrix3D()
        mat1.setIdentity()

        if key == 'plus':
            # mat1.setMatMove(0, 0, -300)
            mat1.setMatScale(*self.__center_location.get_points(),
                             1.1, 1.1, 1.1)


        elif key == 'minus':
            # mat1.setMatMove(0, 0, 300)
            mat1.setMatScale(*self.__center_location.get_points(),
                             1 / 1.1, 1 / 1.1, 1 / 1.1)


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
                self.play_coin(int(key))
                self.__cur_state.setIdentity()
            except IndexError:
                pass
            finally:
                return

        self.__cur_state = mat1
        # self.prepare_and_draw_all()
