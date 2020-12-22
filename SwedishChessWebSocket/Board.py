bigfigs = ['l', 'k', 's', 'r', 'f']
dirD = {'l': [(1, 0, 8), (-1, 0, 8), (0, 1, 8), (0, -1, 8)],
        's': [(1, 1, 8), (-1, 1, 8), (-1, -1, 8), (1, -1, 8)],
        'k': [(2, 1, 1), (-2, 1, 1), (2, -1, 1), (-2, -1, 1),
              (1, 2, 1), (-1, 2, 1), (1, -2, 1), (-1, -2, 1)],
        'r': [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1),
              (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
        'f': [(1, 0, 8), (-1, 0, 8), (0, 1, 8), (0, -1, 8),
              (1, 1, 8), (-1, 1, 8), (-1, -1, 8), (1, -1, 8)]}
D = {'w': 0, 'b': 1}


# ! - шах
# ? - инвалидный ход

class Cell:
    def __init__(self, figure='.', color='.'):
        self.figure = figure
        self.color = color


class Board:
    def __init__(self):
        self.field = [[Cell() for _ in range(8)] for _ in range(8)]
        self.r = {'w': (0, 4), 'b': (7, 4)}
        self.r_moved = {'w': False, 'b': False}
        self.l_moved = {'w0': False, 'w7': False, 'b0': False, 'b7': False}
        self.turn = 'w'

    def __getitem__(self, i):
        return self.field[i]

    def __setitem__(self, i, a):
        self.field[i] = a

    def start(self):
        fig_set = ['l', 'k', 's', 'f', 'r', 's', 'k', 'l']
        self[0] = [Cell(fig_set[i], 'w') for i in range(8)]
        self[1] = [Cell('p', 'w') for _ in range(8)]
        self[6] = [Cell('p', 'b') for _ in range(8)]
        self[7] = [Cell(fig_set[i], 'b') for i in range(8)]

    def display(self):
        for i in range(7, -1, -1):
            for j in range(8):
                print(self[i][j].color, self[i][j].figure, sep='', end=' ')
            print()

    def moves(self, s_x, s_y, check=False):
        moves = []
        Cell = self[s_x][s_y]
        if Cell.figure in bigfigs:
            D = dirD[Cell.figure]
            for d in D:  # d имеет формат (шаг по x, шаг по y, range), например (+1, -1, 1)
                x, y = s_x, s_y
                dx, dy, r = d
                i, tag = 0, True
                while i < r and tag:
                    x, y = x + dx, y + dy
                    if x not in range(8) or y not in range(8):
                        tag = False
                    elif self[x][y].figure == '.':
                        moves.append((x, y))
                    elif self[x][y].color == Cell.color:
                        tag = False
                    elif self[x][y].figure == 'r':
                        if check:
                            moves.append((x, y))
                        tag = False
                    else:
                        moves.append((x, y))
                        tag = False
                    i += 1

        elif Cell.figure == 'p':
            dP = {'w': 1, 'b': -1}
            dx = dP[Cell.color]

            if self[s_x + dx][s_y].color == '.' and not check:
                moves.append((s_x + dx, s_y))
            if s_y < 7 and self[s_x + dx][s_y + 1].color not in ['.', Cell.color] and (
                    self[s_x + dx][s_y + 1].figure != 'r' or check):
                moves.append((s_x + dx, s_y + 1))
            if s_y > 0 and self[s_x + dx][s_y - 1].color not in ['.', Cell.color] and (
                    self[s_x + dx][s_y - 1].figure != 'r' or check):
                moves.append((s_x + dx, s_y - 1))
            if s_y < 7 and self[s_x + dx][s_y + 1].color == '.' and check:
                moves.append((s_x + dx, s_y + 1))
            if s_y > 0 and self[s_x + dx][s_y - 1].color == '.' and check:
                moves.append((s_x + dx, s_y - 1))

            sP = {'w': 1, 'b': 6}
            if s_x == sP[Cell.color] and (self[s_x + dx][s_y].color, self[s_x + 2 * dx][s_y].color) == (
                    '.', '.') and not check:
                moves.append((s_x + 2 * dx, s_y))

        return moves

    def check(self, color):
        for i in range(8):
            for j in range(8):
                if self[i][j].color not in ['.', color]:
                    M = self.moves(i, j, check=True)
                    if self.r[color] in M:
                        return True
        return False

    def castling(self, color, direction):
        castD = {'w': 0, 'b': 7}
        castF = {'l': (0, 5, 0), 'r': (4, 8, 7)}

        x = castD[color]
        a, b, rook = castF[direction]

        if self.r_moved[color] or self.l_moved[color + str(rook)]:
            return 'Invalid Move'

        for y in range(a + 1, b - 1):
            if self[x][y].figure != '.':
                return 'Path not Clear'

        for i in range(8):
            for j in range(8):
                if self[i][j].color not in ['.', color]:
                    M = self.moves(i, j, check=True)
                    for y in range(a, b):
                        if self[x][y] in M:
                            return 'Path under Attack'

        self[x][5].figure = 'l'
        self[x][rook].figure = 'r'
        self.r[color] = (x, rook)
        self.r_moved[color] = True

    def checkmate(self, color):
        for start_x in range(8):
            for start_y in range(8):
                if self[start_x][start_y].color == color:
                    M = self.moves(start_x, start_y)
                    for m in M:
                        end_x, end_y = m
                        nextBoard = Board()
                        nextBoard.field = [[self[i][j] for j in range(8)] for i in range(8)]
                        nextBoard.r = self.r

                        nextBoard[end_x][end_y] = Cell(nextBoard[start_x][start_y].figure, color)
                        nextBoard[start_x][start_y] = Cell()
                        if nextBoard[end_x][end_y].figure == 'r':
                            nextBoard.r[color] = (end_x, end_y)

                        if not nextBoard.check(color):
                            del nextBoard
                            return False
                elif self[start_x][start_y].color == '.':
                    nextBoard = Board()
                    nextBoard.field = [[self[i][j] for j in range(8)] for i in range(8)]
                    nextBoard.r = self.r

                    nextBoard[start_x][start_y] = Cell('f', color)
                    if not nextBoard.check(color):
                        del nextBoard
                        return 'Must place a figure'
        return True


class Game:  # создаем игру
    def __init__(self, n=2):  # задаем число досок/полей
        self.Boards = [Board() for i in range(n)]
        for i in range(n):
            self.Boards[i].start()

    def move(self, index, start, end):
        start_x, start_y = (int(start[1]) - 1, ord(start[0]) - ord('a'))
        end_x, end_y = (int(end[1]) - 1, ord(end[0]) - ord('a'))

        currBoard = self.Boards[index]
        if currBoard[start_x][start_y].color != currBoard.turn:
            return 'Not Yout Turn'

        M = currBoard.moves(start_x, start_y)

        if (end_x, end_y) in M:
            temp_fig = currBoard[end_x][end_y].figure
            curr_fig = currBoard[start_x][start_y].figure
            curr_col = currBoard[start_x][start_y].color

            nextBoard = Board()
            nextBoard.field = [[currBoard[i][j] for j in range(8)] for i in range(8)]
            nextBoard.r = currBoard.r

            nextBoard[end_x][end_y] = Cell(curr_fig, curr_col)
            nextBoard[start_x][start_y] = Cell()
            if curr_fig == 'r':
                nextBoard.r[curr_col] = (end_x, end_y)
                nextBoard.r_moved[curr_col] = True
            if curr_fig == 'l' and start_y in [0, 7]:
                nextBoard.l_moved[curr_col + str(curr_col)] = True

            if nextBoard.check(curr_col):
                del nextBoard
                return '?'

            self.Boards[index] = nextBoard
            del currBoard

            tempD = {'w': 'b', 'b': 'w'}
            self.Boards[index].turn = tempD[curr_col]
            self.Boards[index].display()
            return temp_fig
        return '!'

    def get_color(self, index):
        return self.Boards[index].turn

    def display_moves(self, index, start):
        start_x, start_y = (int(start[1]) - 1, ord(start[0]) - ord('a'))

        currBoard = self.Boards[index]
        M = currBoard.moves(start_x, start_y)

        for i in range(7, -1, -1):
            for j in range(8):
                if (i, j) in M and currBoard[i][j].color == '.':
                    print('**', sep='', end=' ')
                elif (i, j) in M and currBoard[i][j].color != '.':
                    print('*' + currBoard[i][j].figure, sep='', end=' ')
                else:
                    print(currBoard[i][j].color, currBoard[i][j].figure, sep='', end=' ')
            print()

    def add_figure(self, index, position, asg_figure, color):
        Asgar = {'R': 'l',
                 'N': 'k',
                 'B': 's',
                 'Q': 'f',
                 'P': 'p'}

        currBoard = self.Boards[index]
        x, y = (int(position[1]) - 1, ord(position[0]) - ord('a'))
        if color != currBoard.turn:
            return 'Not Yout Turn'
        figure = Asgar[asg_figure]

        nextBoard = Board()
        nextBoard.field = [[currBoard[i][j] for j in range(8)] for i in range(8)]

        if nextBoard[x][y].color == '.' and (figure != 'p' or x not in [0, 7]):
            nextBoard[x][y] = Cell(figure, color)
            if nextBoard.check('w') or nextBoard.check('b'):
                del nextBoard
                return '!'

            self.Boards[index] = nextBoard
            del currBoard

            tempD = {'w': 'b', 'b': 'w'}
            self.Boards[index].turn = tempD[color]

            self.Boards[index].display()
            return figure
        return '!'
