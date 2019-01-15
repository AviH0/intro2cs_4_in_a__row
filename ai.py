from game import Game
import numpy as np
class AI:

    def __init__(self, game, player):
        self.ai_num=player
        self.other_ai_num= 0
        if player %2 ==0:
            self.other_ai_num = 1
        else:
            self.other_ai_num=2
        self.game=game
        self.ROWS_NUM = 6
        self.COLS_NUM = 7
        self.cells = []
        for i in range(self.ROWS_NUM):
            self.cells.append([])
            for x in range(self.COLS_NUM):
                self.cells[i].append(0)

    def find_legal_move(self, timeout=None):
        # return self.find_move_helper()
        options = self.find_relevant_cells()
        options = {option[1]: 0 for option in options}
        options = self.think(options, self.ai_num)
        return max(options.keys(), key=lambda value: options[value])


    def update_board(self,column,player):
        for row in range(5,-1,-1):
            if self.cells[row][column]==0:
                self.cells[row][column]=player
                break
    def find_relevant_cells(self):
        lst=[]
        for col in range(self.COLS_NUM):
            if self.cells[0][col] == 0:
                for row in range(5, -1, -1):
                    if self.cells[row][col]==0:
                        lst.append((row,col))

                        break
        return lst

    def create_game(self, moves):
        game = Game()
        for i in range(6):
            for j in range(7):
                game.cells[i][j] = self.game.get_player_at(i, j)
        for move in moves:
            try:
                game.make_move(int(move))
            except ValueError:
                pass
        return game

    def think(self, options_dict, player, moves=""):
        game = self.create_game(moves)
        options = {option: 0 for option in options_dict.keys()}
        winner = game.get_winner()
        last_move = 1
        if moves:
            last_move = int(moves[-1])
        if len(moves) > 2:
            return {last_move:-1}
        if winner == self.ai_num:
            return {last_move:1}
        if winner == self.other_ai_num:
            return {last_move:-1}
        for option in options.keys():
            if player == self.ai_num:
                options[option] += sum(self.think(options, self.other_ai_num, moves + str(option)))
            else:
                options[option] += sum(self.think(options, self.ai_num, moves))
        return options



    def find_move_helper(self,col=None,turn=0):
        if turn==0:
            lst=self.find_relevant_cells()
            for item in lst:
                row=item[0]
                col=item[1]
                self.cells[row][col]=self.ai_num
                if self.get_winner()== self.ai_num:
                    self.cells[row][col] = 0
                    return col
                self.cells[row][col] = 0
            for item in lst:
                row=item[0]
                col=item[1]
                self.cells[row][col]=self.other_ai_num
                if self.get_winner()== self.other_ai_num:
                    self.cells[row][col] = 0
                    return col
                self.cells[row][col] = 0
            return lst[0][1]

        else:
            for col in range(self.COLS_NUM):
                if self.cells[self.ROWS_NUM - 1][col] == 0:
                    for row in range (5,-1,-1):
                        if self.cells[row][col]==0:
                            self.cells[row][col]= self.other_ai_num
                            if self.get_winner()== self.other_ai_num:
                                self.cells[row][col] = 0
                                return False
                            self.cells[row][col]=0
                            break
            return True

    def get_winner(self):
        """go over a row:"""
        seq=""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                seq+=str(self.cells[row][col])
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq = ""

        "go over col"
        for col in range(self.COLS_NUM):
            for row in range(self.ROWS_NUM):
                seq += str(self.cells[row][col])
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq = ""
        "go over aobliques"
        matrix= np.asarray(self.cells)
        diags = [matrix[::-1, :].diagonal(i) for i in range(-5, 7)]
        diags.extend(matrix.diagonal(i) for i in range(6, -7, -1))
        lst= ([n.tolist() for n in diags])
        new_lst=[]
        for x in lst:
            if len(x) >3:
                new_lst.append(x)
        for line in new_lst:
            for x in line:
                seq+=str(x)
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq=""
        return None

    def change_cur_player(self):
        if self.current_player==1:
            self.current_player=2
        else:
            self.current_player=1

    def get_player_at(self, row, col):
        if row>5 or row<0:
            raise ValueError("illegal move")
        if col >6 or col <0:
            raise ValueError("illegal move")
        if self.cells[row][col] == 0:
            return None
        return self.cells[row][col]

    def get_current_player(self):
        return self.current_player

    def print_board(self):
        st=""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                st+= str(self.cells[row][col])
            print(st)
            st=""

    def get_last_found_move(self):
        pass
