from copy import deepcopy

class KingStepError(Exception):
    pass

class ColorError(Exception):
    pass

class KingCheckWarning(Exception):
    pass

class Data:
    _coordinates = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    _rev_coordinates = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    
class Figure(Data):
    def __init__(self, color=None, inherit_board=None):
        self.color = color  # get color while initializing
        self.inherit_board = inherit_board  # get inheritance from board
    
    def reform_coordinates(self, old, new): # transform coordinates to normal
        old_vertical = 8 - int(old[1])
        old_horizontal = self._coordinates[old[0]]
        new_vertical = 8 - int(new[1])
        new_horizontal = self._coordinates[new[0]]
        return old_vertical, old_horizontal, new_vertical, new_horizontal

class Pawn(Figure):
    def __init__(self, color=None, inherit_board=None):
        super().__init__(color, inherit_board)  # inheritance from ABC Piece
        self.first_step = True  # get availability to step by two squares

    def __str__(self):  # get correct output
        if self.color == "white":
            return "P"
        return "p"

    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if self.inherit_board.board[new_vertical][new_horizontal] == ".":
            if old_horizontal == new_horizontal:
                if self.first_step:
                    self.first_step = False
                    return (new_vertical - old_vertical <= 2 if self.color == "black" else old_vertical - new_vertical <= 2)
                return new_vertical - old_vertical <= 1 if self.color == "black" else old_vertical - new_vertical <= 1
        else:
            if (self.color == "white" and abs(new_horizontal - old_horizontal) == 1 and (old_vertical - new_vertical) == 1) \
            or (self.color == "black" and abs(new_horizontal - old_horizontal) == 1 and (new_vertical - old_vertical) == 1):
                if self.color != self.inherit_board.board[new_vertical][new_horizontal].color:
                    self.inherit_board.kill(old, new, self.color)
                    return True
        return False



class Rook(Figure):
    
    def __str__(self):  # get correct output
        if self.color == "white":
            return "R"
        return "r"
    
    def check_road(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if old_vertical == new_vertical:
            for i in range(min(old_horizontal, new_horizontal), max(old_horizontal, new_horizontal)):
                if self.inherit_board.board[new_vertical][i] != ".":
                    return False
        else:
            for i in range(min(old_vertical, new_vertical), max(old_vertical, new_vertical, new_horizontal)):
                if self.inherit_board.board[i][new_vertical] != ".":
                    return False
        return True
    
    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if self.inherit_board.board[new_vertical][new_horizontal] == ".":
            return self.check_road(old, new) and (new_horizontal == old_horizontal or new_vertical == old_vertical)
        if new_horizontal == old_horizontal or new_vertical == old_vertical:
            if self.color != self.inherit_board.board[new_vertical][new_horizontal].color:
                self.inherit_board.kill(old, new, self.color)
                return True
        return False



class Knight(Figure):
    def __str__(self):  # get correct output
        if self.color == "white":
            return "N"
        return "n"
    
    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if self.inherit_board.board[new_vertical][new_horizontal] == ".":
            return ((abs(old_horizontal - new_horizontal) == 2) and (abs(old_vertical - new_vertical) == 1)) or \
                ((abs(old_horizontal - new_horizontal) == 1) and (abs(old_vertical - new_vertical) == 2))
        else:
            if self.color != self.inherit_board.board[new_vertical][new_horizontal].color:
                self.inherit_board.kill(old, new, self.color)
                return True
        return False


class Bishop(Figure):
    def __str__(self):  # get correct output
        if self.color == "white":
            return "B"
        return "b"
    
    def check_road(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        for i in range(min(old_vertical, new_vertical), max(old_vertical, new_vertical)):
            for j in range(min(old_horizontal, new_horizontal), max(old_horizontal, new_horizontal)):
                if max(old_vertical, new_vertical) - i == max(old_horizontal, new_horizontal) - j:
                    if self.inherit_board.board[i][j] != ".":
                        return False
        return True
    
    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if abs(new_horizontal - old_horizontal) == abs(new_vertical - old_vertical):
            if self.inherit_board.board[new_vertical][new_horizontal] == ".":
                    ab = abs(new_horizontal - old_horizontal)
                    return self.check_road(old, new) and ((old_horizontal + ab) < 8 or (new_horizontal + ab) < 8) and ((old_vertical + ab) < 8 or (new_vertical + ab) < 8)
            else:
                if self.color != self.inherit_board.board[new_vertical][new_horizontal].color:
                    self.inherit_board.kill(old, new, self.color)
                    return self.check_road(old, new) and ((old_horizontal + ab) < 8 or (new_horizontal + ab) < 8) and ((old_vertical + ab) < 8 or (new_vertical + ab) < 8)
        return False


class Queen(Figure):
    def __str__(self):  # get correct output
        if self.color == "white":
            return "Q"
        return "q"
    
    def check_road(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        for i in range(min(old_vertical, new_vertical), max(old_vertical, new_vertical)):
            for j in range(min(old_horizontal, new_horizontal), max(old_horizontal, new_horizontal)):
                if max(old_vertical, new_vertical) - i == max(old_horizontal, new_horizontal) - j:
                    if self.inherit_board.board[i][j] != ".":
                        return False
        if old_vertical == new_vertical:
            for i in range(min(old_horizontal, new_horizontal), max(old_horizontal, new_horizontal)):
                if self.inherit_board.board[new_vertical][i] != ".":
                    return False
        else:
            for i in range(min(old_vertical, new_vertical), max(old_vertical, new_vertical, new_horizontal)):
                if self.inherit_board.board[i][new_vertical] != ".":
                    return False
        return True
    
    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if (abs(old_horizontal - new_horizontal) == abs(old_vertical - new_vertical)) or ((old_horizontal == new_horizontal) or (old_vertical == new_vertical)):
            if self.inherit_board.board[new_vertical][new_horizontal] == ".":
                ab = abs(new_horizontal - old_horizontal)
                return self.check_road(old, new) and ((old_horizontal + ab) < 8 or (new_horizontal + ab) < 8) and ((old_vertical + ab) < 8 or (new_vertical + ab) < 8)
            else:
                if self.color != self.inherit_board.board[new_vertical][new_horizontal].color:
                    self.inherit_board.kill(old, new, self.color)
                    ab = abs(new_horizontal - old_horizontal)
                    return self.check_road(old, new) and ((old_horizontal + ab) < 8 or (new_horizontal + ab) < 8) and ((old_vertical + ab) < 8 or (new_vertical + ab) < 8)
        return False


class King(Figure):
    def __str__(self):  # get correct output
        if self.color == "white":
            return "K"
        return "k"
    
    def check_move(self, old, new):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        dang =  []
        for x in range(8):
            for y in range(8):
                if self.inherit_board.board[x][y] != "." and self.inherit_board.board[x][y].color != self.color and \
                str(self.inherit_board.board[x][y]).lower() != str(self).lower():
                    dang.append(self.inherit_board.board[x][y].check_move(self._rev_coordinates[y] + str(8 - x), new))
        dang = not any(dang)
        if self.inherit_board.board[new_vertical][new_horizontal] == ".":
            if dang and (abs(new_horizontal - old_horizontal) <= 1 and abs(new_vertical - old_vertical) <= 1):
                return True
            else:
                if dang and (abs(new_horizontal - old_horizontal) <= 1 and abs(new_vertical - old_vertical) <= 1):
                    self.inherit_board.kill(old, new)
                    return True
        raise KingStepError("Король в опасности!")

class Board(Data):

    def __init__(self):
        self.board = []  # create an empty board
        self.white_killed = []
        self.black_killed = []

    def create_board(self):  # filling by figure objects
        pawns = [[Pawn("black", self) for _ in range(8)], [Pawn("white", self) for _ in range(8)]]
        other_black = [Rook("black", self), Knight("black", self), Bishop("black", self), Queen("black", self),
                       King("black", self), Bishop("black", self), Knight("black", self), Rook("black", self)]
        other_white = [Rook("white", self), Knight("white", self), Bishop("white", self), Queen("white", self),
                       King("white", self), Bishop("white", self), Knight("white", self), Rook("white", self)]
        self.board = [other_black,
                          pawns[0],
                          ["." for _ in range(8)],
                          ["." for _ in range(8)],
                          ["." for _ in range(8)],
                          ["." for _ in range(8)],
                          pawns[1],
                          other_white]
    
    def reform_coordinates(self, old, new):
        old_vertical = 8 - int(old[1])
        old_horizontal = self._coordinates[old[0]]
        new_vertical = 8 - int(new[1])
        new_horizontal = self._coordinates[new[0]]
        return old_vertical, old_horizontal, new_vertical, new_horizontal
    
    def reform_board(self, old, new): # reform board after step
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        self.board[new_vertical][new_horizontal] = self.board[old_vertical][old_horizontal]
        self.board[old_vertical][old_horizontal] = "."
    
    def kill(self, old, new, color):
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if color == "white":
            self.black_killed.append(self.board[new_vertical][new_horizontal])
        else:
            self.white_killed.append(self.board[new_vertical][new_vertical])
        
    
    def check_move_board(self, old, new, color): # checking move
        old_vertical, old_horizontal, new_vertical, new_horizontal = self.reform_coordinates(old, new)
        if isinstance(self.board[old_vertical][old_horizontal], King):
            self.check_check([new_vertical, new_horizontal], color)
        return self.board[old_vertical][old_horizontal].color == color and self.board[old_vertical][old_horizontal].check_move(old, new) # get other method from piece' class
        

    def get_board(self):  # get correct output
        header = "   A B C D E F G H   "
        result = [header + "\n"]
        for index, row in enumerate(self.board):
            result.append(f"{8 - index}  {' '.join(list(map(str, row)))}  {8 - index}")
        result += ["\n" + header]
        return "\n".join(result)

    # def check_check(self, coords, color):
    #     dang = []
    #     kx, ky = coords
        
    #     for x in range(8):
    #         for y in range(8):
    #             if self.board[x][y] != "." and self.board[x][y].color != color and \
    #             str(self.board[x][y]).lower() != "k":
    #                 dang.append(self.board[x][y].check_move(self._rev_coordinates[y] + str(8 - x), self._rev_coordinates[ky] + str(8 - kx)))
    #     if any(dang):
    #         raise KingCheckWarning("Шах!")

    # def check_mate(self, step="white"):  # function which checks if it is mate
    #     count, count_dang = 0, 0
    #     x, y = 0, 0
    #     for i in range(8):
    #         for j in range(8):
    #             if isinstance(self.board[i][j], King) and self.board[i][j].color == step:
    #                 x, y = i, j
    #     for i in range(x - 1 if x != 0 else 0, x + 2 if x != 7 else 8):
    #         for j in range(y - 1 if y != 0 else 0, x + 2 if x != 7 else 8):
    #             try:
    #                 if self.board[i][j] == ".":
    #                     count += 1
    #                     self.board[x][y].check_move(f"{self._rev_coordinates[y]}{7 - j}", f"{self._rev_coordinates[j]}{7 - i}")
    #             except:
    #                 count_dang += 1
    #     return count != count_dang

class Game(Data):
    def __init__(self):
        self.boards = []
        self.current = None
    
    def read_file_full_notation(self, filename):
        board = Board()
        board.create_board()
        self.boards.append(board)
        self.current = 0
        mask = "abcdefgh"
        with open(filename, "r", encoding="utf-8") as file:
            data = [x.split()[1:] for x in file]
            for step in data:
                for i in range(len(step)):
                    current_board = deepcopy(self.boards[-1])
                    if step[i][0] not in mask:
                        if step[i][1] not in mask:
                            step[i] = step[i][2:]
                        else:
                            step[i] = step[i][1:]
                    if step[i].endswith("!!") or step[i].endswith("??"):
                        step[i] = step[i][:-2]
                    if step[i].endswith("!") or step[i].endswith("?")\
                    or step[i].endswith("+") or step[i].endswith("#"):
                        step[i] = step[i][:-1]
                    current_board.reform_board(step[i][:2], step[i][3:])
                    self.boards.append(current_board)                 
    
    def write_to_file(self, filename):
        _specials = {"Кр": lambda x: isinstance(x, King), "Л": lambda x: isinstance(x, Rook), "К": lambda x: isinstance(x, Knight),\
            "С": lambda x: isinstance(x, Bishop), "Ф": lambda x: isinstance(x, Queen), "": lambda x: True}
        with open(filename, "w", encoding="utf-8") as file:
            steps = []
            previous = self.boards[0].board
            temp = ""
            for i in range(1, len(self.boards)):
                temp = "" if i % 2 else temp 
                current = self.boards[i].board
                begin, end, delimiter, special = "", "", "", ""
                for x in range(len(current)):
                    for y in range(len(current)):
                        if previous[x][y] != "." and current[x][y] == ".":
                            begin = f"{self._rev_coordinates[y]}{8 - x}"
                            for sp in _specials:
                                if _specials[sp](previous[x][y]):
                                    special = sp
                                    break
                        elif previous[x][y] == "." and current[x][y] != ".":
                            end = f"{self._rev_coordinates[y]}{8 - x}"
                            delimiter = "-"
                        elif str(previous[x][y]) != str(current[x][y]):
                            end = f"{self._rev_coordinates[y]}{8 - x}"
                            delimiter = ":"
                temp += f"{(i + 1) // 2}. {special}{begin}{delimiter}{end}" if i % 2 else f" {begin}{delimiter}{end}"
                if i % 2 == 0: steps.append(temp)
                previous = current
            if temp != steps[-1]: steps.append(temp)
            for step in steps:
                file.write(step + "\n")
    
    def add_to(self, board):
        self.boards.append(board)
        if self.current is None:
            self.current = 0
    
    def go_forward(self):
        if self.current < len(self.boards) - 1:
            self.current += 1
        else:
            raise IndexError("Это последнее поле")
    
    def go_back(self, n=1):
        if self.current - n >= 0:
            self.current -= n
        else:
            raise IndexError("Произошла ошибка - проблема с возвратом хода!")


def play_full_notation():
    game = Game()
    game.read_file_full_notation("file.txt")
    play = False
    while play is False:
        print(game.boards[game.current].get_board())
        print("Ход белых") if game.current % 2 == 0 else print("Ход черных")
        step = input("Вперед? ")
        if step.lower() == "нет":
            try:
                game.go_back()
            except Exception as e:
                print(e)
        elif step.lower() == "да":
            try:
                game.go_forward()
            except Exception as e:
                print(e)
                end = input("Выйти из игры? ")
                if end.lower() == "да":
                    break
        else:
            play = True
    if play is False:
        return None
    main(board=game.boards[game.current], current_step="white" if game.current % 2 == 0 else "black", game=game)


def main(board=None, current_step="white", game=None):  # gaming function
    if board is None:
        board = Board()  # initialize main board
        board.create_board() # creating the board
    game = Game()
    game.add_to(board)
    while True:  # while game is on
        print(game.boards[-1].get_board())
        while True:
            try:
                step = input(f"Ходят {current_step}. Введите ваш ход (e2e4 e.g.): ")
                if step == "назад":
                    if len(game.boards) > 0:
                        game.boards.pop()
                    else:
                        print("Назад невозможно, это первое поле!")
                elif step == "запись":
                    filename = input("Введите название файла(с .txt): ")
                    game.write_to_file(filename)
                else:
                    if game.boards[-1].check_move_board(step[:2], step[2:], current_step):
                        board = deepcopy(game.boards[-1])
                        board.reform_board(step[:2], step[2:])
                        game.add_to(board)
                        current_step = "black" if current_step == "white" else "white"
                    else:
                        raise Exception
            except Exception as e:
                print("Произошла ошибка ввода!")
            else:
                break

main()