from tkinter import *
from tkinter import messagebox, simpledialog
import random
from colors import Colors


class Board:

    def __init__(self):
        self.window = Tk()
        self.window.title('2048')
        self.gameArea = Frame(self.window, bg='azure3')
        self.size = int(simpledialog.askstring("Input", "Enter size of the board", parent=self.window))
        self.board = []
        self.matrix = [[0] * self.size for i in range(self.size)]
        self.shifted = False
        self.merged = False
        self.moved = False

        for i in range(self.size):
            rows = []
            for j in range(self.size):
                l = Label(self.gameArea, text='', bg='azure4',
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)
                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()

    def insert_num(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    empty_cells.append((i, j))

        if len(empty_cells) == 0:
            return False
        insert_at = random.choice(empty_cells)
        i = insert_at[0]
        j = insert_at[1]
        self.matrix[i][j] = random.choice([2, 4])

    def can_merge(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True

        for i in range(self.size - 1):
            for j in range(self.size):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def merge_left(self):
        # self.merged=False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.merged = True

    def merge_right(self):
        for i in range(self.size):
            for j in range(self.size - 1, 0, -1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j - 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j - 1] = 0
                    self.merged = True

    def transpose(self):
        self.matrix = [list(t) for t in zip(*self.matrix)]

    def shift_right(self):
        for i in range(self.size):
            zero = self.size - 1
            for j in range(self.size - 1, -1, -1):
                if self.matrix[i][j] != 0:
                    self.matrix[i][j], self.matrix[i][zero] = self.matrix[i][zero], self.matrix[i][j]
                    if zero != j:
                        self.shifted = True
                    zero -= 1

    def shift_left(self):
        for i in range(self.size):
            zero = 0
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    self.matrix[i][j], self.matrix[i][zero] = self.matrix[i][zero], self.matrix[i][j]
                    if zero != j:
                        self.shifted = True
                    zero += 1

    def paint_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.matrix[i][j]),
                                            bg=Colors.bg_color.get(str(self.matrix[i][j])),
                                            fg=Colors.color.get(str(self.matrix[i][j])))


class Game():
    def __init__(self, panel):

        self.gamepanel = panel
        self.size = self.gamepanel.size
        self.over = False

    def start(self):
        self.gamepanel.insert_num()
        self.gamepanel.insert_num()
        self.gamepanel.paint_grid()
        self.gamepanel.window.bind('<Key>', self.link_keys)
        self.gamepanel.window.mainloop()

    def link_keys(self, event):
        if self.over:
            return
        self.gamepanel.shifted = False
        self.gamepanel.merged = False
        self.gamepanel.moved = False
        pressed_key = event.keysym
        if pressed_key == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.shift_left()
            self.gamepanel.merge_left()
            self.gamepanel.moved = self.gamepanel.shifted or self.gamepanel.merged
            self.gamepanel.shift_left()
            self.gamepanel.transpose()
        elif pressed_key == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.shift_right()
            self.gamepanel.merge_right()
            self.gamepanel.moved = self.gamepanel.shifted or self.gamepanel.merged
            self.gamepanel.shift_right()
            self.gamepanel.transpose()
        elif pressed_key == 'Left':
            self.gamepanel.shift_left()
            self.gamepanel.merge_left()
            self.gamepanel.moved = self.gamepanel.shifted or self.gamepanel.merged
            self.gamepanel.shift_left()
        elif pressed_key == 'Right':
            self.gamepanel.shift_right()
            self.gamepanel.merge_right()
            self.gamepanel.moved = self.gamepanel.shifted or self.gamepanel.merged
            self.gamepanel.shift_right()

        else:
            pass
        self.gamepanel.paint_grid()

        flag = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.gamepanel.matrix[i][j] == 2048:
                    flag = 1
                    break
        if flag == 1:
            self.over = True
            messagebox.showinfo('2048', message='You Wonnn!!')
            print("won")
            return
        for i in range(self.size):
            for j in range(self.size):
                if self.gamepanel.matrix[i][j] == 0:
                    flag = 1
                    break
        if not (flag or self.gamepanel.can_merge()):
            self.over = True
            messagebox.showinfo('2048', 'Game Over!!!')
            print("Over")
        if self.gamepanel.moved:
            self.gamepanel.insert_num()

        self.gamepanel.paint_grid()


gamepanel = Board()
game2048 = Game(gamepanel)
game2048.start()
