import tkinter as tk
import tkinter.messagebox
from game import Game
from .graphics import Graphics
from ai import AI
import os


class Gui:
    # Files:
    PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
    START = os.path.join(PATH, 'start.png')
    PVP = os.path.join(PATH, 'PvP.png')
    PVC = os.path.join(PATH, 'pvc.png')
    PCVPC = os.path.join(PATH, 'cvc.png')
    CVP=os.path.join(PATH, 'cvp.png')
    # Messages:
    WELCOME_MSG = 'Welcome to Connect Four!'
    ILLEGAL_MOVE_MSG = '--Illegal Move!--'
    AI_ERR_MSG = "AI Error!"
    VICTORY_MSG = 'Player {} Won! \n Do You Want To Play Again?'
    GAME_OVER_MESSAGE = 'Game Over!'
    TIE="its a tie!"

    # Game modes:
    PVP_MODE = 'PVP'
    PVPC_MODE = 'PVPC'
    PCVPC_MODE = 'PCVPC'
    PCVP_MODE = 'ccvp'
    # Player types:
    PC = 'PC'
    HUMAN = 'Human'

    # Keys:
    UP_KEY = 'Up'
    DOWN_KEY = 'Down'
    LEFT_KEY = 'Left'
    RIGHT_KEY = 'Right'
    ZOOM_IN_KEY = 'plus'
    ZOOM_OUT_KEY = 'minus'

    def __init__(self):
        self.__root = tk.Tk()
        self.__load_rescources()
        self.__welcome()
        self.__root.mainloop()

    def __load_rescources(self):
        self.__start_image = tk.PhotoImage(file=self.START)
        self.__p_v_p = tk.PhotoImage(file=self.PVP)
        self.__p_v_pc = tk.PhotoImage(file=self.PVC)
        self.__pc_v_pc = tk.PhotoImage(file=self.PCVPC)
        self.__pc_v_p=tk.PhotoImage(file=self.CVP)

    def __welcome(self):
        "when game starts, create these:"
        start_frame = tk.Frame(self.__root)

        welcome_label = tk.Label(start_frame, text=self.WELCOME_MSG)
        welcome_label.pack()

        start_button = tk.Button(start_frame,
                                 image=self.__start_image,
                                 command=self.__start_menu, relief=tk.FLAT)
        start_button.pack()
        start_frame.pack()

    def __start_menu(self):
        "create mode-buttons and pack them"
        old_stuff = self.__root.pack_slaves()
        for thing in old_stuff:
            thing.destroy()
        options = tk.Frame(self.__root)

        p_v_p_button = tk.Button(options, image=self.__p_v_p,
                                 command=lambda: self.__start_game(
                                     mode=self.PVP_MODE),
                                 relief=tk.FLAT)
        p_v_pc_button = tk.Button(options, image=self.__p_v_pc,
                                  command=lambda: self.__start_game(
                                      mode=self.PVPC_MODE),
                                  relief=tk.FLAT)
        pc_v_pc_button = tk.Button(options, image=self.__pc_v_pc,
                                   command=lambda: self.__start_game(
                                       mode=self.PCVPC_MODE),
                                   relief=tk.FLAT)
        pc_v_p_button = tk.Button(options, image=self.__pc_v_p,
                                   command=lambda: self.__start_game(
                                       mode=self.PCVP_MODE),
                                   relief=tk.FLAT)

        pc_v_pc_button.pack()
        p_v_p_button.pack()
        p_v_pc_button.pack()
        pc_v_p_button.pack()
        options.pack()

    def __start_game(self, mode):
        "agter a mode pressed, this function starts the relevant mode"
        game = Game()
        ai_turn=None
        slaves = self.__root.pack_slaves()
        for slave in slaves:
            slave.destroy()
        self.__mode = mode
        canvas = tk.Canvas(self.__root)
        graphics = Graphics(canvas)
        canvas.pack()
        if mode == self.PCVPC_MODE:
            ai1 = AI(game, 1)
            ai2 = AI(game, 2)
            self.__bot_vs_bot(game, graphics, ai1, ai2)
            self.__current_player = self.PC
        elif mode == self.PVPC_MODE:
            ai1=AI(game,2)
            ai_turn=2
            self.__current_player = self.HUMAN
        elif mode==self.PCVP_MODE:
            ai_turn=1
            ai1 = AI(game, 1)
            self.__play_ai_move(game, graphics, ai1, 1)
            self.__current_player = self.HUMAN
        else:
            ai1 = None
            self.__current_player = self.HUMAN
        self.__root.bind('<Key>',
                         lambda event: self.key_pressed(game, graphics, event,
                                                        ai1,ai_turn))

    def __bot_vs_bot(self, game, graphics, ai1, ai2):
        "bot vs bot game:"
        if self.__play_ai_move(game, graphics, ai1, ai1.ai_num):
            self.__root.after(1000,
                              lambda: self.__bot_vs_bot(game, graphics, ai2,
                                                        ai1))

    def key_pressed(self, game, graphics, event, ai=None,turn= None):
        "when there is at least one human player:"
        key = event.keysym
        if event.char.isnumeric() and self.__current_player == self.HUMAN:
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
                        winning_lst=game.winning_cells
                        print(winning_lst)

                        self.__root.after(10, lambda: self.__game_is_over(
                            graphics, winner))
                    if game.is_tie()==True:
                        message = "WANT TO PLAY AGAIN?"
                        play_again = tk.messagebox.askyesno(self.TIE, message)
                        if play_again:
                            graphics.quit()
                            self.__root.after(100, self.__start_menu)
                        else:
                            self.__root.quit()
                            exit(0)
                    elif ai:
                        self.__current_player = self.PC
                        ai.update_board(key, player)
                        self.__root.after(1000,
                                          lambda: self.__play_ai_move(game,
                                                                      graphics,
                                                                      ai, turn))

                except ValueError:
                    graphics.display_message(self.ILLEGAL_MOVE_MSG, 'red')

        if key == self.RIGHT_KEY:
            graphics.move_camera(right=5)
        if key == self.LEFT_KEY:
            graphics.move_camera(left=5)
        if key == self.UP_KEY:
            graphics.move_camera(up=5)
        if key == self.DOWN_KEY:
            graphics.move_camera(down=5)
        if key == self.ZOOM_IN_KEY:
            graphics.move_camera(zoom=1.1)
        if key == self.ZOOM_OUT_KEY:
            graphics.move_camera(zoom=1 / 1.1)

    def __play_ai_move(self, game, graphics, ai, player):
        "do ai move"
        try:
            move = ai.find_legal_move()
            game.make_move(move)
            ai.update_board(move, player)
            graphics.play_coin(move, player)
            if self.__mode == self.PVPC_MODE or self.__mode == self.PCVP_MODE:
                self.__current_player = self.HUMAN
        except RuntimeError:
            self.__game_is_over(graphics, None)
        winner = game.get_winner()
        if winner:
            self.__root.after(10,
                              lambda: self.__game_is_over(graphics,
                                                          winner))
            return False
        return True

    def __game_is_over(self, graphics, winner):
        "if game over, show relevant msg and ask if player wants to play again"
        self.__root.unbind('<Key>')
        message = self.AI_ERR_MSG
        if winner:
            graphics.victory()
            graphics.display_message(self.GAME_OVER_MESSAGE, 'green')
            message = self.VICTORY_MSG.format(
                winner)
        play_again = tk.messagebox.askyesno(self.GAME_OVER_MESSAGE, message)
        if play_again:
            graphics.quit()
            self.__root.after(100, self.__start_menu)
        else:
            self.__root.quit()
            exit(0)
