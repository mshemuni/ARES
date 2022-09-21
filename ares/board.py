import numpy as np
import sys
import pyautogui


np.set_printoptions(threshold=sys.maxsize)


class Board:
    def __init__(self, number: int):
        if number % 2 != 0:
            raise ValueError(f"{number} is not even")
        self.number = number
        self.board = np.empty((self.number, self.number))
        self.board[:] = np.nan
        self.original = self.board.copy()

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def read_from_image(cls, dimention, puzzle):
        a_board = Board(dimention)
        w, h, c = puzzle.shape
        gap = w / dimention
        coords = np.array(
            [
                [
                    [gap / 2 + gap * i, gap / 2 + gap * u]
                    for i in range(dimention)
                ]
                for u in range(dimention)
            ]
        ).astype(int)
        for y, line in enumerate(coords):
            for x, element in enumerate(line):
                if (puzzle[element[0]][element[1]] == [255, 213, 0]).all():
                    a_board.set(x, y, 0)
                elif (puzzle[element[0]][element[1]] == [0, 89, 190]).all():
                    a_board.set(x, y, 1)

        return a_board

    def set(self, x, y, value):
        if value not in [1, 0]:
            raise ValueError("Value only can be either 0 or 1")
        self.board[x][y] = value
        self.original[x][y] = value

    def __other(self, value):
        return (value + 1) % 2

    def __check_gap(self, data, i):
        return data[i] == data[i + 2] and np.isnan(data[i + 1])

    def __check_consecutive(self, data, i):
        to_return = [False, False]
        if data[i] == data[i + 1] and not np.isnan(data[i]):
            if i > 0:
                if np.isnan(data[i - 1]):
                    to_return[0] = True

            if i < len(data) - 2:
                if np.isnan(data[i + 2]):
                    to_return[1] = True

        return to_return

    @classmethod
    def click(cls, board, dimen, x_offset=0, y_offset=0):
        gap = dimen / board.number
        for y in range(board.number):
            for x in range(board.number):
                if np.isnan(board.original[y][x]):
                    the_x, the_y = gap / 2 + gap * x, gap / 2 + gap * y
                    if board.board[y][x] == 0:
                        pyautogui.click(the_x + x_offset, the_y + y_offset)
                    elif board.board[y][x] == 1:
                        pyautogui.rightClick(the_x + x_offset, the_y + y_offset)

    def solve(self):
        while np.isnan(self.board).any():
            for i in range(self.number):

                if np.isnan(self.board[i]).any():
                    if np.isnan(self.board[i]).sum() == 2:
                        if (~np.isnan(self.board).any(axis=1)).any():
                            for x, value in enumerate(~np.isnan(self.board).any(axis=1)):
                                if value:
                                    mask = np.isnan(self.board[i])
                                    if (self.board[i][~mask] == self.board[x][~mask]).all():
                                        self.board[i][mask] = self.board[x][mask][::-1]
                    for k in [0, 1]:
                        if self.board[i][self.board[i] == k].size == self.number / 2:
                            self.board[i][np.isnan(self.board[i])] = self.__other(k)

                    for k in range(self.number - 2):
                        if self.__check_gap(self.board[i], k):
                            self.board[i][k + 1] = self.__other(self.board[i][k])

                    for k in range(self.number - 1):
                        fill_it = self.__check_consecutive(self.board[i], k)
                        if any(fill_it):
                            if fill_it[0]:
                                self.board[i][k - 1] = self.__other(self.board[i][k])

                            if fill_it[1]:
                                self.board[i][k + 2] = self.__other(self.board[i][k])

                if np.isnan(self.board[:, i]).any():
                    if np.isnan(self.board[:, i]).sum() == 2:
                        if (~np.isnan(self.board).any(axis=0)).any():
                            for x, value in enumerate(~np.isnan(self.board).any(axis=0)):
                                if value:
                                    mask = np.isnan(self.board[:, i])
                                    if (self.board[:, i][~mask] == self.board[:, x][~mask]).all():
                                        self.board[:, i][mask] = self.board[:, x][mask][::-1]

                    for k in [0, 1]:
                        if self.board[:, i][self.board[:, i] == k].size == self.number / 2:
                            self.board[:, i][np.isnan(self.board[:, i])] = self.__other(k)

                    for k in range(self.number - 2):
                        if self.__check_gap(self.board[:, i], k):
                            self.board[:, i][k + 1] = self.__other(self.board[:, i][k])

                    for k in range(self.number - 1):
                        fill_it = self.__check_consecutive(self.board[:, i], k)
                        if any(fill_it):
                            if fill_it[0]:
                                self.board[:, i][k - 1] = self.__other(self.board[:, i][k])

                            if fill_it[1]:
                                self.board[:, i][k + 2] = self.__other(self.board[:, i][k])
