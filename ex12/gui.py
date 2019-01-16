import tkinter as tk
import tkinter.messagebox
from game import Game
from .graphics import Graphics
from ai import AI
import os


class Gui:
    # Files:
    PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
    START = PATH + '/images/start.png'
    PVP = PATH + '/images/pvp.png'
    PVC = PATH + '/images/pvc.png'
    PVP_SELECTED = PATH + '/images/PvP-selected.png'
    PVPC_SELECTED = PATH + '/images/PvPC-selected.png'
    PCVPC = PATH + '/images/cvc.png'

    def __init__(self):
        self.__root = tk.Tk()
        self.__load_rescources()
        self.__welcome()
        self.__root.mainloop()

    def __load_rescources(self):
        self.__start_image = tk.PhotoImage(file=self.START)
        self.__p_v_p = tk.PhotoImage(file=self.PVP)
        self.__p_v_pc = tk.PhotoImage(file=self.PVC)
        self.__pvp_selected = tk.PhotoImage(file=self.PVP_SELECTED)
        self.__pvpc_selected = tk.PhotoImage(file=self.PVPC_SELECTED)
        self.__pc_v_pc = tk.PhotoImage(file=self.PCVPC)

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
                                 command=lambda: self.__start_game(mode='PvP'),
                                 relief='flat')
        p_v_pc_button = tk.Button(options, image=self.__p_v_pc,
                                  command=lambda: self.__start_game(
                                      mode='PvPC'),
                                  relief='flat')
        pc_v_pc_button = tk.Button(options, image=self.__pc_v_pc,
                                   command=lambda: self.__start_game(
                                       mode='PCvPC'),
                                   relief='flat')
        pc_v_pc_button.pack()
        p_v_p_button.pack()
        p_v_pc_button.pack()
        options.pack()

    def __start_game(self, mode):
        game = Game()
        current = mode
        # if mode == 'PvP':
        #     button.config(image=self.__pvp_selected)
        # elif mode == "PCvPC":
        #     current = "pcvpc"
        # else:
        #     current = "pvc"
        #     button.config(image=self.__pvpc_selected)

        slaves = self.__root.pack_slaves()
        for slave in slaves:
            slave.destroy()

        canvas = tk.Canvas(self.__root)
        graphics = Graphics(canvas)
        canvas.pack()
        if mode == "PCvPC":
            ai1 = AI(game, 1)
            ai2 = AI(game, 2)
            self.__bot_vs_bot(game, graphics, ai1, ai2)
        if current == "pvc":
            ai1 = AI(game, 1)
            self.__play_ai_move(game, graphics, ai1, 1)
        else:
            ai1 = None
        self.__root.bind('<Key>',
                         lambda event: self.key_pressed(game, graphics, event,
                                                        ai1))

    def __bot_vs_bot(self, game, graphics, ai1, ai2):

        # move = ai1.find_legal_move()
        # game.make_move(move)
        # ai1.update_board(move, 1)
        # graphics.play_coin(move, 1)
        if self.__play_ai_move(game, graphics, ai1, ai1.ai_num):
            self.__root.after(1000,
                              lambda: self.__bot_vs_bot(game, graphics, ai2,
                                                        ai1))

        # move = ai2.find_legal_move()
        # game.make_move(move)
        # ai2.update_board(move, 2)
        # graphics.play_coin(move, 2)

    def key_pressed(self, game, graphics, event, ai=None):
        key = event.keysym
        if event.char.isnumeric():
            key = int(event.char) - 1
            if key < 0 or key > 6:
                pass
            else:
                try:

                    player = game.get_current_player()
                    game.make_move(key)
                    self.__root.after(10, lambda: graphics.play_coin(key,
                                                                     player))

                    winner = game.get_winner()
                    if winner:
                        self.__root.after(10, lambda: self.__game_is_over(
                            graphics, winner))

                    if ai:
                        ai.update_board(key, player)
                        self.__root.after(1000,
                                          lambda: self.__play_ai_move(game,
                                                                      graphics,
                                                                      ai, 1))

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
            graphics.move_camera(zoom=1.1)
        if key == 'minus':
            graphics.move_camera(zoom=1 / 1.1)

    def __play_ai_move(self, game, graphics, ai, player):
        move = ai.find_legal_move()
        game.make_move(move)
        ai.update_board(move, player)
        graphics.play_coin(move, player)
        winner = game.get_winner()
        if winner:
            self.__root.after(10,
                              lambda: self.__game_is_over(graphics,
                                                          winner))
            return False
        return True

    def __game_is_over(self, graphics, winner):
        "player current player won!"

        self.__root.unbind('<Key>')
        graphics.victory()
        graphics.display_message('Game Over!', 'green')
        play_again = tk.messagebox.askyesno('Game Over!',
                                            'Player {} Won! \n Do You Want To Play Again?'.format(
                                                winner))
        if play_again:
            graphics.quit()
            self.__root.after(100, self.__start_menu)
        else:
            self.__root.quit()
            self.__root.destroy()
            exit(0)
