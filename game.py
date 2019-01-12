import numpy as np

class Game:
    def __init__(self):
        self.current_player=1
        self.ROWS_NUM=6
        self.COLS_NUM=7
        self.cells=[]
        for i in range(self.ROWS_NUM):
            self.cells.append([])
            for x in range(self.COLS_NUM):
                self.cells[i].append(0)

    def make_move(self, column):
        if column >6 or column <0:
            raise ValueError("illegal move")
        for row in range(5,-1,-1):
            if self.get_player_at(row,column) is None:
                self.cells[row][column]=self.current_player
                self.change_cur_player()
                return
        raise ValueError("illegal move")
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

# game=Game()
# while  True:
#     game.print_board()
#     print("player",game.get_current_player(),"this is ur turn!")
#     x=input("enter col: ")
#     game.make_move(int(x))
#     if game.get_winner() is not None:
#         print("player",game.get_winner()," won")
#         game.print_board()
#         break