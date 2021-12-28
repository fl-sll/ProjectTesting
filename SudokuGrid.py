import pygame
import time
import numpy as np
from dokusan import generators
from solver import solve,valid
pygame.font.init()

class Grid:
    # Create board for the Sudoku
    grid = np.array(list(str(generators.random_sudoku(avg_rank = 150))))
    bo = grid.reshape(9,9)
    board = bo.astype(int)
    
    # Create the constructor for the object
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # function to update the model
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # set a sketch of a number clicked by the user but not entered yet (preview)
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clears the board
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # Show box that is clicked by the user
    def click(self, pos):
        """
        parameter: pos
        return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("timesnewroman", 30)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    font = pygame.font.SysFont("timesnewroman", 30)
    textfont = pygame.font.SysFont("comicsans", 30)
    text = font.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 555))
    # Draw Strikes
    text = textfont.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 550))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    time = " " + str(minute) + ":" + str(sec)
    return time

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    
    while run:

        play_time = round(time.time() - start)

        # Allocation of keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False
                
                if event.key == pygame.K_KP_ENTER:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            # Allocation of mouse's use
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

main()
pygame.quit()
