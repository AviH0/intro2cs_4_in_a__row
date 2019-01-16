from game import Game
import numpy as np


class AI:

    def __init__(self, game, player):
        self.ai_num = player
        self.other_ai_num = 0
        if player % 2 == 0:
            self.other_ai_num = 1
        else:
            self.other_ai_num = 2
        self.game = game
        self.ROWS_NUM = 6
        self.COLS_NUM = 7
        self.cells = []
        for i in range(self.ROWS_NUM):
            self.cells.append([])
            for x in range(self.COLS_NUM):
                self.cells[i].append(0)

    def find_legal_move(self, timeout=None):
        # return self.find_move_helper()
        options = self.get_possible_moves(self.game)
        options = self.think(self.ai_num, {option: 0 for option in options})
        result = max(options.keys(), key=lambda x: options[x])
        return result

    def update_board(self, column, player):
        for row in range(5, -1, -1):
            if self.cells[row][column] == 0:
                self.cells[row][column] = player
                break

    def find_relevant_cells(self):
        lst = []
        for col in range(self.COLS_NUM):
            if self.cells[0][col] == 0:
                for row in range(5, -1, -1):
                    if self.cells[row][col] == 0:
                        lst.append((row, col))

                        break
        return lst

    def create_game(self, my_moves, his_moves):
        game = Game()
        for i in range(6):
            for j in range(7):
                game.cells[i][j] = self.game.get_player_at(i, j)
        for i in range(max(len(my_moves), len(his_moves))):
            try:
                if len(my_moves) > i:
                    game.make_move(int(my_moves[i]))
                if len(his_moves) > i:
                    game.make_move(int(his_moves[i]))
            except ValueError:
                return False
        return game

    def get_possible_moves(self, game):
        lst = []
        for i in range(7):
            if not game.cells[0][i]:
                lst.append(i)
        return lst

    def find_relevant(self, cells):
        lst = []
        for col in range(self.COLS_NUM):
            if cells[0][col] == 0:
                for row in range(5, -1, -1):
                    if cells[row][col] == 0:
                        lst.append((row, col))

                        break
        return lst

    def think_mat(self, mat, player, depth = 0):
        relevants = self.find_relevant(mat)
        good, bad = self.analyze_board(mat)
        if player == self.other_ai_num:
            if bad:
                return [-1000]
            if good > 1:
                return [50]
            if good == 1:
                return [good]
        if player == self.ai_num:
            if good:
                return [100]
            # if not good and not bad:
            #     return [50]
        if depth > 3:
            return [0]
        results = []
        for option in relevants:
            mat[option[0]][option[1]] = player
            if player == self.ai_num:
                result = self.think_mat(mat, self.other_ai_num, depth+1)[0], option[1]
            else:
                result = self.think_mat(mat, self.ai_num, depth + 1)[0], option[1]
            results.append(result)
            mat[option[0]][option[1]] = 0
        if results:
            return max(results, key=lambda value: value[0])
        else:
            return [0]


    def think(self, player, options, my_moves="", his_moves=""):
        game = self.create_game(my_moves, his_moves)
        possibles = self.get_possible_moves(game)
        options = {option: options[option] for option in possibles}
        last_move = 1
        if my_moves:
            last_move = int(my_moves[-1])
        if not game:
            return {last_move: -100}
        winner = game.get_winner()
        if len(my_moves) > 2:
            return {last_move: 0}
        if winner == self.ai_num and len(my_moves) == 1:
            return {last_move: 50}
        if winner == self.ai_num:
            return {last_move: 5}
        if winner == self.other_ai_num and len(my_moves) == 1:
            return {last_move: -10}
        if winner == self.other_ai_num:
            return {last_move: -5}
        for option in options.keys():
            if player == self.ai_num:
                result = self.think(self.other_ai_num, options, my_moves + str(option),
                                    his_moves)
                options[option] = sum(result.values())
            else:
                options[option] = sum(self.think(self.ai_num, options, my_moves,
                                                  his_moves + str(
                                                      option)).values())
        return options

    def analyze_board(self, mat):
        board = mat[:]
        good = 0
        bad = 0
        for row in board:
            row = str(row)
            if '0, 1, 1, 1' in row or '1, 1, 1, 0' in row:
                good += 1
            if '0, 2, 2, 2' in row or '2, 2, 2, 0' in row:
                bad += 1
        for row in np.transpose(board):
            row = str(row)
            if '0, 1, 1, 1' in row or '1, 1, 1, 0' in row:
                good += 1
            if '0, 2, 2, 2' in row or '2, 2, 2, 0' in row:
                bad += 1
        for diagonal in list(self.diags(board)):
            diagonal = str(diagonal)
            if '0, 1, 1, 1' in diagonal or '1, 1, 1, 0' in diagonal:
                good += 1
            if '0, 2, 2, 2' in diagonal or '2, 2, 2, 0' in diagonal:
                bad += 1
        return good, bad

    def diags(self, mat):
        width, height = len(mat[0]), len(mat)

        def diag(sx, sy):
            for x, y in zip(range(sx, height), range(sy, width)):
                yield mat[x][y]

        for sx in range(height):
            yield list(diag(sx, 0))
        for sy in range(1, width):
            yield list(diag(0, sy))

    def find_move_helper(self, col=None, turn=0):
        if turn == 0:
            lst = self.find_relevant_cells()
            for item in lst:
                row = item[0]
                col = item[1]
                self.cells[row][col] = self.ai_num
                if self.get_winner() == self.ai_num:
                    self.cells[row][col] = 0
                    return col
                self.cells[row][col] = 0
            for item in lst:
                row = item[0]
                col = item[1]
                self.cells[row][col] = self.other_ai_num
                if self.get_winner() == self.other_ai_num:
                    self.cells[row][col] = 0
                    return col
                self.cells[row][col] = 0
            return lst[0][1]

        else:
            for col in range(self.COLS_NUM):
                if self.cells[self.ROWS_NUM - 1][col] == 0:
                    for row in range(5, -1, -1):
                        if self.cells[row][col] == 0:
                            self.cells[row][col] = self.other_ai_num
                            if self.get_winner() == self.other_ai_num:
                                self.cells[row][col] = 0
                                return False
                            self.cells[row][col] = 0
                            break
            return True

    def get_winner(self):
        """go over a row:"""
        seq = ""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                seq += str(self.cells[row][col])
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
        matrix = np.asarray(self.cells)
        diags = [matrix[::-1, :].diagonal(i) for i in range(-5, 7)]
        diags.extend(matrix.diagonal(i) for i in range(6, -7, -1))
        lst = ([n.tolist() for n in diags])
        new_lst = []
        for x in lst:
            if len(x) > 3:
                new_lst.append(x)
        for line in new_lst:
            for x in line:
                seq += str(x)
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq = ""
        return None

    def change_cur_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def get_player_at(self, row, col):
        if row > 5 or row < 0:
            raise ValueError("illegal move")
        if col > 6 or col < 0:
            raise ValueError("illegal move")
        if self.cells[row][col] == 0:
            return None
        return self.cells[row][col]

    def get_current_player(self):
        return self.current_player

    def print_board(self):
        st = ""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                st += str(self.cells[row][col])
            print(st)
            st = ""

    def get_last_found_move(self):
        pass
