from .matrix_3D import Matrix3D, Point3D
from .board import Board
from .shapes import Shapes
from .table import Table
from .room import Room
import math
import time


class Graphics:
    # Files:
    FLOOR_FILE = 'ex12/floor.obj'
    TEXT_FILE = 'ex12/text.obj'
    PLAYER_FILE = 'ex12/player.obj'
    NUMBER_1_FILE = 'ex12/number_1.obj'
    NUMBER_2_FILE = 'ex12/number_2.obj'

    # Tags:
    FLOOR_TAG = 'Floor'
    TEXT_TAG = 'Text'
    PLAYER_TAG = 'Player'
    NUMBER_1_TAG = 'Number_1'
    NUMBER_2_TAG = 'Number_2'

    # Canvas:
    HEIGHT = 900
    WIDTH = 900
    BACKGROUND_COLOR = 'grey'

    # Points:
    DEPTH = 5000
    MAGOZ = WIDTH / 2, HEIGHT / 3, DEPTH
    CENTER_LOCATION = 0, 0, DEPTH
    LIGHT_SOURCE = 500, 500, 4900

    # Location:
    BOARD_LOCATION = CENTER_LOCATION[0] + 0, CENTER_LOCATION[1] + 0, \
                     CENTER_LOCATION[2] + 200

    TABLE_LOCATION = CENTER_LOCATION[0] + 0, CENTER_LOCATION[1] + 850, \
                     CENTER_LOCATION[2] + 0

    ROOM_LOCATION = CENTER_LOCATION[0] + 0, CENTER_LOCATION[1] + 850, \
                    CENTER_LOCATION[2] + -1000

    FLOOR_LOCATION = CENTER_LOCATION[0] + 0, CENTER_LOCATION[1] + 850, \
                     CENTER_LOCATION[2] + -1000

    TEXT_LOCATION = CENTER_LOCATION[0] + 0, CENTER_LOCATION[1] + 850, \
                    CENTER_LOCATION[2] + -1000

    PLAYER_DISPLAY_OFFSET = -15, -25, -25

    # Colors:

    TABLE_COLOR = 'darkorange4'
    BOARD_COLOR = 'blue4'
    WALL_COLOR = 'aquamarine4'
    FLOOR_COLOR = 'grey10'
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'

    def __init__(self, canvas, player_1_color=RED, player_2_color=GREEN):

        # Configure Canvas:
        self.__canvas = canvas
        self.__canvas.configure(height=self.HEIGHT, width=self.WIDTH,
                                bg=self.BACKGROUND_COLOR)
        # self.__canvas.master.bind('<Key>', self.__key_pressed)

        # Environment points:
        self.magoz = Point3D(*self.MAGOZ)
        self.__light_source = Point3D(*self.LIGHT_SOURCE)
        self.__room_light_source = Point3D(
            *self.LIGHT_SOURCE)  # (500, 0, 5000)

        # Create all the shapes:
        self.__init_shapes(player_1_color, player_2_color)


        # Build the shapes
        self.__build_shapes()

        # Create the points:
        self.__init_points()

        # Player handles:
        self.__players = [self.__player_1, self.__player_2]
        self.__player_colors = [self.__player_1_color, self.__player_2_color]
        self.__current_player = 0

        # Create the matrix and set the first transformation:
        self.__first_transformation()

        # Initiate the lists for the coins and for the column pointers:
        self.__coins = []
        self.__active_coins = []
        self.__column_points = []

        # Create all the coins and place_holders:
        self.__create_coins_and_place_holders()

        # Save the time of initiation for the timer:
        self.__time = time.time()

        # Create the Timer:
        self.__canvas.create_text(170, 30, text='TIME:', fill='red',
                                  font="Century 25 bold", tags='time')

        # Make the first call to redraw:
        self.prepare_and_draw_all()

    def __build_shapes(self):
        # Build all the shapes:
        self.__board.build_shape(*self.BOARD_LOCATION)
        self.__table.build_shape(*self.TABLE_LOCATION)
        self.__room.build_shape(*self.ROOM_LOCATION)
        self.__floor.build_shape(*self.FLOOR_LOCATION)
        self.__text.build_shape(*self.TEXT_LOCATION)
        self.__player_display_location = Point3D(
            self.__board.get_board_top().x + self.PLAYER_DISPLAY_OFFSET[0],
            self.__board.get_board_top().y + self.PLAYER_DISPLAY_OFFSET[1],
            self.__board.get_board_top().z + self.PLAYER_DISPLAY_OFFSET[2])
        self.__player.build_shape(*self.__player_display_location.get_points())
        self.__player_1.build_shape(
            *self.__player_display_location.get_points())
        self.__player_2.build_shape(
            *self.__player_display_location.get_points())

    def __init_points(self):
        # Create Points:
        self.__center_location = Point3D(*self.CENTER_LOCATION)


    def __init_shapes(self, player_1_color, player_2_color):
        # Get RGB colors:
        table_color = self.__canvas.winfo_rgb(self.TABLE_COLOR)
        board_color = self.__canvas.winfo_rgb(self.BOARD_COLOR)
        wall_color = self.__canvas.winfo_rgb(self.WALL_COLOR)
        floor_color = self.__canvas.winfo_rgb(self.FLOOR_COLOR)
        black = self.__canvas.winfo_rgb(self.BLACK)
        self.__player_1_color = self.__canvas.winfo_rgb(player_1_color)
        self.__player_2_color = self.__canvas.winfo_rgb(player_2_color)
        # Create all Shapes:
        self.__table = Table(self.magoz, self.__light_source, table_color)
        self.__floor = Shapes(self.magoz, self.__room_light_source,
                              self.FLOOR_FILE,
                              floor_color, self.FLOOR_TAG)
        self.__room = Room(self.magoz, self.__room_light_source, wall_color)
        self.__text = Shapes(self.magoz, self.__room_light_source,
                             self.TEXT_FILE,
                             black, self.TEXT_TAG)
        self.__board = Board(self.magoz, self.__light_source, board_color)
        self.__player = Shapes(self.magoz, self.__light_source,
                               self.PLAYER_FILE, board_color,
                               self.PLAYER_TAG)
        self.__player_1 = Shapes(self.magoz, self.__light_source,
                                 self.NUMBER_1_FILE, self.__player_1_color,
                                 self.NUMBER_1_TAG)
        self.__player_2 = Shapes(self.magoz, self.__light_source,
                                 self.NUMBER_2_FILE, self.__player_2_color,
                                 self.NUMBER_2_TAG)
        self.__shapes = [self.__table, self.__floor, self.__room, self.__text,
                         self.__board, self.__player, self.__player_1,
                         self.__player_2]

    def __first_transformation(self):
        self.__cur_state = Matrix3D()
        temp = Matrix3D()
        # temp.setMatScale(*self.__center_location.get_points(), 1.5,
        #                  1.5, 1.5)
        self.__cur_state.mullMatMat(temp)
        temp.setMatRotateXFix(math.pi / 45,
                              *self.__center_location.get_points())
        self.__cur_state.mullMatMat(temp)

    def prepare_and_draw_all(self):

        # Transform all the shapes with the current matrix:
        for shape in self.__shapes:
            shape.mull_points(self.__cur_state)
            shape.real_to_guf()
        self.__center_location.mull_point(self.__cur_state)
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

        # Draw all the relevant shapes for the current view:
        self.__room.convert_and_show(self.__canvas, self.__center_location.z)

        if self.__text.get_middle().z > self.__board.get_middle().z:
            self.__text.convert_and_show(self.__canvas)

        if self.__floor.get_middle().z > self.__board.get_board_top().z:
            self.__floor.convert_and_show(self.__canvas)

        if self.__board.get_board_top().z < self.__table.get_middle().z:
            self.__table.convert_and_show(self.__canvas)

        self.__board.convert_and_show_back(self.__canvas)
        for coin in self.__active_coins:
            coin.convert_and_show(self.__canvas)
        self.__board.convert_and_show_front(self.__canvas)
        self.__player.convert_and_show(self.__canvas)
        self.__players[self.__current_player].convert_and_show(
            self.__canvas)

        if self.__board.get_board_top().z >= self.__table.get_middle().z:
            self.__table.convert_and_show(self.__canvas)


        # Reset the matrix:
        self.__cur_state.setIdentity()

        # Update the timer:
        self.__update_clock()

        # Set the mainloop to redraw:
        self.__canvas.master.after(100, self.prepare_and_draw_all)

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
        point = 1 + len(self.__column_points[column])
        self.__animate_coin(point, coin, dx, dy, dz)

    def __animate_coin(self, point, coin, dx, dy, dz, x0=0, y0=0, z0=0, i=1):

        matrix = Matrix3D()

        ax = (2 * dx / (point ** 2))
        ay = (2 * dy / (point ** 2))
        az = (2 * dz / (point ** 2))
        ddx = 0.5 * ax * i ** 2
        ddy = 0.5 * ay * i ** 2
        ddz = 0.5 * az * i ** 2
        matrix.setMatMove(ddx - x0, ddy - y0, ddz - z0)
        x0 = ddx
        y0 = ddy
        z0 = ddz
        coin.mull_points(matrix)
        self.__cur_state.setIdentity()
        if i < point:
            self.__canvas.master.after(80,
                                       lambda: self.__animate_coin(point, coin,
                                                                   dx, dy, dz,
                                                                   x0, y0, z0,
                                                                   i + 1))

    def __create_coins_and_place_holders(self):
        for i in range(7):
            self.__coins.append([])
            self.__column_points.append([])
            for j in range(6):
                point = Point3D(self.__board.get_board_top().x - 170 + 56 * i,
                                self.__board.get_board_top().y + 40 + 48 * j,
                                self.__board.get_middle().z)
                self.__column_points[i].append(point)

                new_coin = Shapes(self.magoz, self.__light_source,
                                  "ex12/coin.obj", (0, 0, 0),
                                  'item%s%s' % (i, j))
                self.__coins[i].append(new_coin)
                new_coin.build_shape(self.__board.get_board_top().x - 170 + 56 * i,
                                     self.__board.get_board_top().y,
                                     self.__board.get_middle().z)

    def __update_clock(self):
        time_now = time.time() - self.__time
        time_now = time.gmtime(time_now)
        str_time = '%02d : %02d : %02d' % (
            time_now.tm_hour, time_now.tm_min, time_now.tm_sec)
        self.__canvas.tag_raise('time')
        self.__canvas.itemconfig('time', text='TIME: ' + str_time)

    def move_camera(self, **kwargs):
        mat1 = Matrix3D()
        if 'right' in kwargs.keys():
            angle = -math.radians(kwargs['right'])
            mat1.setMatRotateAxis(*self.__board.get_board_top().get_points(),
                                  *self.__board.get_board_bottom().get_points(), angle)
            self.__cur_state.mullMatMat(mat1)

        if 'left' in kwargs.keys():
            angle = math.radians(kwargs['left'])
            mat1.setMatRotateAxis(*self.__board.get_board_top().get_points(),
                                  *self.__board.get_board_bottom().get_points(), angle)
            self.__cur_state.mullMatMat(mat1)

        if 'zoom' in kwargs.keys():  # mat1.setMatMove(0, 0, -300)
            mat1.setMatScale(*self.__center_location.get_points(),
                             kwargs['zoom'], kwargs['zoom'], kwargs['zoom'])
            self.__cur_state.mullMatMat(mat1)

        if 'up' in kwargs.keys():
            angle = -math.radians(kwargs['up'])
            mat1.setMatRotateXFix(angle,
                                  *self.__center_location.get_points())
            self.__cur_state.mullMatMat(mat1)

        if 'down' in kwargs.keys():
            angle = math.radians(kwargs['down'])
            mat1.setMatRotateXFix(angle,
                                  *self.__center_location.get_points())
            self.__cur_state.mullMatMat(mat1)


    # def __key_pressed(self, event):
    #
    #     key = event.keysym
    #     mat1 = Matrix3D()
    #     mat1.setIdentity()
    #
    #     if key == 'plus':
    #         # mat1.setMatMove(0, 0, -300)
    #         mat1.setMatScale(*self.__center_location.get_points(),
    #                          1.1, 1.1, 1.1)
    #
    #
    #     elif key == 'minus':
    #         # mat1.setMatMove(0, 0, 300)
    #         mat1.setMatScale(*self.__center_location.get_points(),
    #                          1 / 1.1, 1 / 1.1, 1 / 1.1)
    #
    #
    #     elif key == 'Up':
    #         angle = math.pi / 45
    #         mat1.setMatRotateXFix(angle, *self.__center_location.get_points())
    #
    #     elif key == 'Down':
    #         angle = -math.pi / 45
    #         mat1.setMatRotateXFix(angle, *self.__center_location.get_points())
    #
    #     elif key == 'Left':
    #         angle = -math.pi / 45
    #         mat1.setMatRotateAxis(*self.__board.get_board_top().get_points(),
    #                               *self.__board.get_board_bottom().get_points(), angle)
    #
    #     elif key == 'Right':
    #         angle = math.pi / 45
    #         mat1.setMatRotateAxis(*self.__board.get_board_top().get_points(),
    #                               *self.__board.get_board_bottom().get_points(), angle)
    #
    #     elif key.isnumeric():
    #         try:
    #             self.play_coin(int(key))
    #             self.__cur_state.setIdentity()
    #         except IndexError:
    #             pass
    #         finally:
    #             return
    #
    #     self.__cur_state = mat1