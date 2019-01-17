import numpy as np

class Game:
    def __init__(self):
        self.current_player=1
        self.ROWS_NUM=6
        self.COLS_NUM=7
        self.cells=[]
        self.winning_cells=[]
        for i in range(self.ROWS_NUM):
            self.cells.append([])
            for x in range(self.COLS_NUM):
                self.cells[i].append(0)

    def is_tie(self):
        "checks if all cells filled"
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                if self.cells[row][col]==0:
                    return False
        return True

    def get_winning_cells(self,line,value):
        "after there's a winner, update the winning cells"
        last=0
        if line=="row":
            for col in range(self.COLS_NUM):
                if len(self.winning_cells)==4:
                    break
                if last != self.cells[value][col]:
                    self.winning_cells=[]
                self.winning_cells.append((value,col))
                last=self.cells[value][col]
        elif line=="col":
            for row in range(self.ROWS_NUM):
                if len(self.winning_cells)==4:
                    break
                if last != self.cells[row][value]:
                    self.winning_cells=[]
                self.winning_cells.append((row,value))
                last=self.cells[row][value]

    def make_move(self, column):
        "make move function- by col"
        if column >6 or column <0:
            raise ValueError("illegal move")
        for row in range(5,-1,-1):
            if self.get_player_at(row,column) is None:
                self.cells[row][column]=self.current_player
                self.change_cur_player()
                return
        raise ValueError("illegal move")
    def get_winner(self):
        "runs over the cells and finds if there's a winner!"
        """go over a row:"""
        seq=""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                seq+=str(self.cells[row][col])
            if "1111" in seq:
                self.get_winning_cells("row",row)
                return 1
            if "2222" in seq:
                self.get_winning_cells("row", row)
                return 2
            seq = ""
        "go over col"
        for col in range(self.COLS_NUM):
            for row in range(self.ROWS_NUM):
                seq += str(self.cells[row][col])
            if "1111" in seq:
                self.get_winning_cells("col", col)
                return 1
            if "2222" in seq:
                self.get_winning_cells("col", col)
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
        "change the player who is playing now"
        if self.current_player==1:
            self.current_player=2
        else:
            self.current_player=1

    def get_player_at(self, row, col):
        "returns the player at a specific cell"
        if row>5 or row<0:
            raise ValueError("illegal move")
        if col >6 or col <0:
            raise ValueError("illegal move")
        if self.cells[row][col] == 0:
            return None
        return self.cells[row][col]

    def get_current_player(self):
        "returns the current playing player"
        return self.current_player

    def print_board(self):
        "prints board"
        st=""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                st+= str(self.cells[row][col])
            print(st)
            st=""
