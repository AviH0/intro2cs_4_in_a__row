import tkinter as tk
from game import Game
from .graphics import Graphics


class Gui:

    def __init__(self):
        self.__root = tk.Tk()

        self.__load_rescources()
        self.__welcome()
        self.__root.mainloop()


    def __load_rescources(self):
        self.__start_image = tk.PhotoImage(file='ex12/images/start.png')
        self.__p_v_p = tk.PhotoImage(file='ex12/images/pvp.png')
        self.__p_v_pc = tk.PhotoImage(file='ex12/images/pvc.png')
        self.__pvp_selected = tk.PhotoImage(file='ex12/images/PvP-selected.png')
        self.__pvpc_selected = tk.PhotoImage(file='ex12/images/PvPC-selected.png')


    def __welcome(self):
        start_frame = tk.Frame(self.__root)

        welcome_label = tk.Label(start_frame, text='Welcome to Connect Four!')
        welcome_label.pack()

        start_button = tk.Button(start_frame,
                                 image=self.__start_image,
                                 command=self.__start_menu, relief='flat')
        start_button.pack()
        start_frame.pack()

    def __start_menu(self):
        old_stuff = self.__root.pack_slaves()
        for thing in old_stuff:
            thing.destroy()
        options = tk.Frame(self.__root)

        p_v_p_button = tk.Button(options, image=self.__p_v_p,
                                 command=lambda: self.__start_game(p_v_p_button, mode='PvP'),
                                 relief='flat')
        p_v_pc_button = tk.Button(options, image=self.__p_v_pc,
                                  command=lambda: self.__start_game(
                                      p_v_pc_button, mode='PvPC' ), relief='flat')
        p_v_p_button.pack()
        p_v_pc_button.pack()
        options.pack()

    def __start_game(self, button, mode):
        if mode == 'PvP':
            button.config(image=self.__pvp_selected)
        else:
            button.config(image=self.__pvpc_selected)

        slaves = self.__root.pack_slaves()
        for slave in slaves:
            slave.destroy()
        game = Game()

        canvas = tk.Canvas(self.__root)
        graphics = Graphics(canvas)
        canvas.pack()
        self.__root.bind('<Key>', lambda event: self.key_pressed(game, graphics, event))

    def key_pressed(self, game, graphics, event):
        key = event.keysym
        if event.char.isnumeric():
            key = int(event.char)
            if key < 0 or key > 6:
                pass
            else:
                try:
                    game.make_move(key)
                    graphics.play_coin(key)
                    if game.get_winner() is not None:
                        "player current player won!"
                        self.__root.unbind('<Key>')
                        graphics.victory()
                except ValueError:
                    graphics.display_message('--Illegal Move!--', 'red')

        if key == 'Right':
            graphics.move_camera(right=5)
        if key == 'Left':
            graphics.move_camera(left=5)
        if key == 'Up':
            graphics.move_camera(up=5)
        if key == 'Down':
            graphics.move_camera(down=5)
        if key == 'plus':
            graphics.move_camera(zoom=1.5)
        if key == 'minus':
            graphics.move_camera(zoom=1/1.5)


