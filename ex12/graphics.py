from .matrix_3D import Matrix3D, Point3D
from .board import Board
from .shapes import Shapes
from .table import Table
from .room import Room
import os
import tkinter
import math
import time



class Graphics:
    # Files:
    PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
    FLOOR_FILE = PATH + '/floor.obj'
    TEXT_FILE = PATH + '/text.obj'
    PLAYER_FILE = PATH + '/player.obj'
    NUMBER_1_FILE = PATH + '/number_1.obj'
    NUMBER_2_FILE = PATH + '/number_2.obj'
    COIN_FILE = PATH + '/coin.obj'

    # Tags:
    FLOOR_TAG = 'Floor'
    TEXT_TAG = 'Text'
    PLAYER_TAG = 'Player'
    NUMBER_1_TAG = 'Number_1'
    NUMBER_2_TAG = 'Number_2'
    TIMER_TAG = 'Timer'
    COIN_TAG = 'item%s%s'
    MSG_TAG = 'Message'
    HELP_TAG = 'Help'

    # Game:
    NUM_ROWS = 6
    NUM_COLUMNS = 7

    # Workaround to get the screen dimensions without instantiating the class:
    temp = tkinter.Tk()
    temp.withdraw()
    temp.after(1, temp.quit)
    temp.mainloop()

    # Canvas:
    HEIGHT = temp.winfo_screenheight() - 100
    WIDTH = temp.winfo_screenwidth() - 10
    BACKGROUND_COLOR = 'grey'
    temp.destroy()

    # Points:
    DEPTH = 5000
    MAGOZ = WIDTH / 2, HEIGHT / 3, DEPTH
    CENTER_LOCATION = 0, 100, DEPTH
    LIGHT_SOURCE = 500, 500, 4900

    # Locations:
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
    HELP_LOCATION = 450, HEIGHT - 50
    MSG_LOCATION = WIDTH / 2, 500
    TIMER_LOCATION = 170, 30

    # Colors:

    TABLE_COLOR = 'darkorange4'
    BOARD_COLOR = 'blue4'
    WALL_COLOR = 'aquamarine4'
    FLOOR_COLOR = 'grey10'
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'

    # Fonts:
    TIMER_FONT = "Century 25 bold"
    MSG_FONT = "Calibri 70 bold"
    HELP_FONT = "Calibri 15 bold"

    # Strings:
    TIMER_TEXT = "TIME: "
    TIME_TEXT = '%02d : %02d : %02d'
    HELP_TEXT = 'Use numbers 1-7 to make a move, `-` and `+` to zoom and the' \
                ' directional keys to move the camera'

    def __init__(self, canvas, player_1_color=RED, player_2_color=GREEN):
        """
        Create an instance of graphics on a canvas.
        :param canvas: A Tkinter Canvas to work on.
        :param player_1_color: A string with a color for the first player.
        :param player_2_color: A string with a color for the second player.
        """

        # Configure Canvas:
        self.__canvas = canvas
        self.__canvas.configure(height=self.HEIGHT, width=self.WIDTH,
                                bg=self.BACKGROUND_COLOR)

        self.__canvas.master.geometry(
            "%dx%d%+d%+d" % (self.WIDTH, self.HEIGHT, 0, 0))
        self.__canvas.master.resizable(height=False, width=False)

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
        self.__current_player = self.__players[0]

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
        self.__canvas.create_text(*self.TIMER_LOCATION, text=self.TIMER_TEXT,
                                  fill=self.RED,
                                  font=self.TIMER_FONT, tags=self.TIMER_TAG)

        # Create the help inforamtion display:
        self.__canvas.create_text(*self.HELP_LOCATION, text=self.HELP_TEXT,
                                  fill=self.GREEN,
                                  font=self.HELP_FONT, tags=self.MSG_TAG)

        # Flag to see if loop should continue.
        self.__still_alive = True

        # Make the first call to redraw:
        self.prepare_and_draw_all()

    def __build_shapes(self):
        """
        Build all the shapes.
        """
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
        """
        Initialise 3D pointers.
        """
        # Create Points:
        self.__center_location = Point3D(*self.CENTER_LOCATION)

    def __init_shapes(self, player_1_color, player_2_color):
        """
        Initialise all the shapes to be displayed in this graphics instance.
        :param player_1_color: A string with a color for the first player.
        :param player_2_color: A string with a color for the second player.
        """
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
        self.__shapes = [self.__floor, self.__room, self.__text, self.__table,
                         self.__board, self.__player, self.__player_1,
                         self.__player_2]
        self.__shapes_order = {shape: i for shape, i in
                               enumerate(self.__shapes)}

    def __first_transformation(self):
        """
        Bring all the objects to their initial location.
        """

        # Initialise the matrix:
        self.__cur_state = Matrix3D()

        # Create a matrix with a scaling transformation and mull it with the
        # main matrix:
        temp = Matrix3D()
        temp.set_mat_scale(*self.__center_location.get_points(), 1.5,
                           1.5, 1.5)
        self.__cur_state.mull_mat_mat(temp)

        # Create a matrix with a rotation transformation and mull it with the
        # main matrix:
        temp.set_mat_rotate_x_fix(math.pi / 45,
                                  *self.__center_location.get_points())
        self.__cur_state.mull_mat_mat(temp)

        # Scale up the room and floor:
        mat = Matrix3D()
        mat.set_mat_scale(*self.__floor.get_middle().get_points(), 2.5, 2.5, 2.5)
        self.__floor.mull_points(mat)
        self.__room.mull_points(mat)

    def prepare_and_draw_all(self):
        """
        Update all the shape's positions according to the matrix, and redraw
        them accordingly.
        """

        # Transform all the shapes with the current matrix and make them update
        # their faces, (except for those that we don't want to show:
        for shape in self.__shapes:
            shape.mull_points(self.__cur_state)
            shape.real_to_guf()
        self.__center_location.mull_point(self.__cur_state)
        for column in self.__coins:
            for coin in column:
                coin.mull_points(self.__cur_state)
        for coin in self.__active_coins:
            coin.mull_points(self.__cur_state)
            coin.real_to_guf()
        for column in self.__column_points:
            for point in column:
                point.mull_point(self.__cur_state)

        # Draw all the relevant shapes in the correct order for the current
        # view:
        self.__room.draw(self.__canvas, self.__center_location.z)
        self.__floor.draw(self.__canvas)

        # If the text is behind the board, show it:
        if self.__text.get_middle().z > self.__board.get_middle().z:
            self.__text.draw(self.__canvas)

        # If the table is tilted forwards, show it now before the board:
        if self.__board.get_board_top().z < self.__table.get_middle().z:
            self.__table.draw(self.__canvas)

        # Show the back of the board, then the coins, and then the front side:
        self.__board.draw_back(self.__canvas)
        for coin in self.__active_coins:
            coin.draw(self.__canvas)
        self.__board.draw_front(self.__canvas)

        # Show the current player display
        self.__player.draw(self.__canvas)
        self.__current_player.draw(self.__canvas)

        # If the table is tilted backwards, show it now:
        if self.__board.get_board_top().z >= self.__table.get_middle().z:
            self.__table.draw(self.__canvas)

        # Reset the matrix:
        self.__cur_state.set_identity()

        # Update the timer:
        self.__update_clock()

        # Make sure the message is visible:
        self.__canvas.tag_raise(self.MSG_TAG)

        # Set the mainloop to redraw:
        if self.__still_alive:
            self.__canvas.master.after(50, self.prepare_and_draw_all)

    def play_coin(self, column, player):
        color = self.__player_colors[player - 1]
        coin_to_play = self.__coins[column].pop()
        coin_to_play.set_color(color)
        self.__active_coins.append(coin_to_play)
        self.__current_player = self.__players[(player - 1) ^ 1]
        self.__place_coin(coin_to_play, column)

    def victory(self):
        self.__current_player = self.__players[self.__players.index(self.__current_player) ^ 1]
        player_mat = Matrix3D()
        player_mat.set_mat_scale(*self.__player.get_middle().get_points(), 1.1,
                                 1.1, 1.1)
        self.__animate_player(player_mat)

    def __animate_player(self, mat, i=1):

        self.__player.mull_points(mat)
        self.__current_player.mull_points(mat)
        if i < 9:
            temp = Matrix3D()
            temp.set_mat_rotate_z_fix(math.radians(10 * ((-1) ** i) / 2 * i),
                                      *self.__player.get_middle().get_points())
            self.__current_player.mull_points(temp)
            self.__player.mull_points(temp)
            self.__canvas.master.after(100, lambda: self.__animate_player(mat,
                                                                          i + 1))
        elif i < 49:
            mat.set_mat_rotate_y_fix(math.pi / 10,
                                     *self.__player.get_middle().get_points())
            self.__canvas.master.after(50, lambda: self.__animate_player(mat,
                                                                         i + 1))

    def display_message(self, msg, color=RED):
        self.__canvas.create_text(*self.MSG_LOCATION, text=msg,
                                  font=self.MSG_FONT, tag=self.MSG_TAG,
                                  fill=color)
        self.__canvas.master.after(2000,
                                   lambda: self.__canvas.delete(self.MSG_TAG))

    def __place_coin(self, coin, column):
        point = self.__column_points[column].pop()
        dx, dy, dz = -coin.get_middle().x + point.x, -coin.get_middle().y + point.y, -coin.get_middle().z + point.z
        point = 1 + len(self.__column_points[column])
        self.__animate_coin(point, coin, dx, dy, dz)

    def __animate_coin(self, num_steps, coin, dx, dy, dz, x0=0, y0=0, z0=0,
                       i=1):

        matrix = Matrix3D()

        # Calculate acceleration in three axes:
        ax = (2 * dx / (num_steps ** 2))
        ay = (2 * dy / (num_steps ** 2))
        az = (2 * dz / (num_steps ** 2))

        # Calculate the distance traveled in this step:
        ddx = 0.5 * ax * i ** 2
        ddy = 0.5 * ay * i ** 2
        ddz = 0.5 * az * i ** 2

        # Set the matrix to move:
        matrix.set_mat_move(ddx - x0, ddy - y0, ddz - z0)

        # Save the current movement factors for the next iteration:
        x0 = ddx
        y0 = ddy
        z0 = ddz

        # Move the coin:
        coin.mull_points(matrix)

        # Set the mainloop to repeat num_steps times:
        if i < num_steps:
            self.__canvas.master.after(40,
                                       lambda: self.__animate_coin(num_steps,
                                                                   coin,
                                                                   dx, dy, dz,
                                                                   x0, y0, z0,
                                                                   i + 1))

    def __create_coins_and_place_holders(self):
        for i in range(self.NUM_COLUMNS):
            self.__coins.append([])
            self.__column_points.append([])
            for j in range(self.NUM_ROWS):
                point = Point3D(self.__board.get_board_top().x - 170 + 56 * i,
                                self.__board.get_board_top().y + 40 + 48 * j,
                                self.__board.get_middle().z)
                self.__column_points[i].append(point)

                new_coin = Shapes(self.magoz, self.__light_source,
                                  self.COIN_FILE, None,
                                  self.COIN_TAG % (i, j))
                self.__coins[i].append(new_coin)
                new_coin.build_shape(
                    self.__board.get_board_top().x - 170 + 56 * i,
                    self.__board.get_board_top().y,
                    self.__board.get_middle().z)

    def __update_clock(self):
        time_now = time.time() - self.__time
        time_now = time.gmtime(time_now)
        str_time = self.TIME_TEXT % (
            time_now.tm_hour, time_now.tm_min, time_now.tm_sec)
        self.__canvas.tag_raise(self.TIMER_TAG)
        self.__canvas.itemconfig(self.TIMER_TAG,
                                 text=self.TIMER_TEXT + str_time)

    def mark_victory(self, coords, color=WALL_COLOR):
        for coord in coords:
            self.__canvas.itemconfig(self.COIN_TAG % coord, fill=color)
        self.__canvas.update_idletasks()

    def quit(self):
        self.__still_alive = False

    def move_camera(self, **kwargs):
        mat1 = Matrix3D()
        if 'right' in kwargs.keys():
            angle = math.radians(kwargs['right'])
            mat1.set_mat_rotate_axis(*self.__board.get_board_top().get_points(),
                                     *self.__board.get_board_bottom().get_points(),
                                     angle)
            self.__cur_state.mull_mat_mat(mat1)

        if 'left' in kwargs.keys():
            angle = -math.radians(kwargs['left'])
            mat1.set_mat_rotate_axis(*self.__board.get_board_top().get_points(),
                                     *self.__board.get_board_bottom().get_points(),
                                     angle)
            self.__cur_state.mull_mat_mat(mat1)

        if 'zoom' in kwargs.keys():
            if self.__board.get_big_y() - self.__board.get_small_y() < 350 and \
                    kwargs['zoom'] < 1:
                return
            mat1.set_mat_scale(*self.__center_location.get_points(),
                               kwargs['zoom'], kwargs['zoom'], kwargs['zoom'])
            self.__cur_state.mull_mat_mat(mat1)

        if 'up' in kwargs.keys():
            if self.__floor.get_big_z() - self.__floor.get_small_z() < 1000:
                return
            angle = math.radians(kwargs['up'])
            mat1.set_mat_rotate_x_fix(angle,
                                      *self.__center_location.get_points())
            self.__cur_state.mull_mat_mat(mat1)

        if 'down' in kwargs.keys():
            if self.__floor.get_big_y() - self.__floor.get_small_y() < 1000:
                return
            angle = -math.radians(kwargs['down'])
            mat1.set_mat_rotate_x_fix(angle,
                                      *self.__center_location.get_points())
            self.__cur_state.mull_mat_mat(mat1)
