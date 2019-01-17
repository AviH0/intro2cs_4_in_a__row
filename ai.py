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
        "finds a leagel move, and returns it"
        if self.game.get_winner():
            raise RuntimeError("No possible AI moves")
        options = self.get_possible_moves(self.game, self.ai_num)
        if not options:
            raise RuntimeError("No possible AI moves")
        options = self.think(self.ai_num)
        move = self.find_move_helper(self.game.cells, self.ai_num)
        if move:
            return move
        result = max(options.keys(), key=lambda x: options[x])
        return result

    def update_board(self, column, player):
        "update self.cells"
        for row in range(5, -1, -1):
            if self.cells[row][column] == 0:
                self.cells[row][column] = player
                break

    def find_relevant_cells(self, cells):
        "finds all possible slots for a move and returns a list of them"
        lst = []
        for col in range(self.COLS_NUM):
            if not cells[0][col]:
                for row in range(5, -1, -1):
                    if not cells[row][col]:
                        lst.append((row, col))

                        break
        return lst

    def create_game(self, my_moves, his_moves):
        "creates a copy of  game"
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

    def get_possible_moves(self, game, player):
        """Get a list of current legal moves. if there is one obvious move,
        return it"""
        lst = []
        move = self.find_move_helper(game.cells, player)
        if move:
            return [move]
        for i in range(7):
            if not game.cells[0][i]:
                lst.append(i)
        return lst

    def think(self, player, my_moves="", his_moves=""):
        """
        Go Over all the possible moves in a depth of 4. count the victories
        and return them.
        """
        last_move = 1
        if my_moves:
            last_move = int(my_moves[-1])

        if len(my_moves) > 2:
            return {last_move: 0}
        game = self.create_game(my_moves, his_moves)
        if not game:
            return {last_move: -100}
        possibles = self.get_possible_moves(game, player)
        options = {option: 0 for option in possibles}

        winner = game.get_winner()
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
                result = self.think(self.other_ai_num, my_moves + str(option),
                                    his_moves)
                options[option] += sum(result.values())
            else:
                options[option] += sum(self.think(self.ai_num, my_moves,
                                                  his_moves + str(
                                                      option)).values())
        return options

    def find_move_helper(self, cells, player):
        """
        If there is an obvious move (one play victory for either side), find
        it.
        """
        lst = self.find_relevant_cells(cells)
        ai_num = player
        if player == 1:
            other_ai_num = 2
        else:
            other_ai_num = 1
        for item in lst:
            row = item[0]
            col = item[1]
            cells[row][col] = ai_num
            if self.get_winner(cells) == ai_num:
                cells[row][col] = None
                return col
            cells[row][col] = None
        for item in lst:
            row = item[0]
            col = item[1]
            cells[row][col] = other_ai_num
            if self.get_winner(cells) == other_ai_num:
                cells[row][col] = None
                return col
            cells[row][col] = None
        return None

    def get_winner(self, cells):
        """go over a row:"""
        seq = ""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                seq += str(cells[row][col])
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq = ""

        "go over col"
        for col in range(self.COLS_NUM):
            for row in range(self.ROWS_NUM):
                seq += str(cells[row][col])
            if "1111" in seq:
                return 1
            if "2222" in seq:
                return 2
            seq = ""
        "go over aobliques"
        matrix = np.asarray(cells)
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
        "changes the current player"
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def get_player_at(self, row, col):
        "returns player at a specific cell"
        if row > 5 or row < 0:
            raise ValueError("illegal move")
        if col > 6 or col < 0:
            raise ValueError("illegal move")
        if self.cells[row][col] == 0:
            return None
        return self.cells[row][col]

    def get_current_player(self):
        "gets tje player who is playing now"
        return self.current_player

    def print_board(self):
        "prints board"
        st = ""
        for row in range(self.ROWS_NUM):
            for col in range(self.COLS_NUM):
                st += str(self.cells[row][col])
            print(st)
            st = ""

    def get_last_found_move(self):
        pass
