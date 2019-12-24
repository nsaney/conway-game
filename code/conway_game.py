#!/usr/bin/env python3

###### Imports ######
import tkinter as tk
from random import random
from collections import deque


###### Constants ######
TITLE = "Conway's Game of Life"
CELL_SIZE = 25
WIDTH = 800
HEIGHT = WIDTH
COLS = int(WIDTH / CELL_SIZE)
ROWS = int(HEIGHT / CELL_SIZE)
MATRIX_UPDATE_MS = 100
CONWAY_LIVE_MIN = 2
CONWAY_LIVE_MAX = 3
CONWAY_BORN_MIN = 3
CONWAY_BORN_MAX = 3
BG_COLOR = 'blue'
FG_LINE = 'white'
FG_CELL = 'red'


###### Variables ######
GENERATION_COUNT = 0


###### Main Method ######
def main():  
  # see https://www.tutorialspoint.com/python3/tk_canvas.htm
  top = tk.Tk()
  top.title(TITLE)
  canvas = tk.Canvas(top, bg = BG_COLOR, width = WIDTH, height = HEIGHT)
  canvas.pack()
  canvas_cells = createMatrix()
  drawGridLines(canvas)
  
  # see https://stackoverflow.com/a/9457884
  matrices = deque([createMatrix(), createMatrix()])
  
  # see https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)
  matrices[0][1+5][2] = True
  matrices[0][2+5][3] = True
  matrices[0][3+5][1] = True
  matrices[0][3+5][2] = True
  matrices[0][3+5][3] = True
  drawMatrix(top, canvas, canvas_cells, matrices[0])
  
  repeatedlyUpdateMatrixDbuf(top, canvas, canvas_cells, matrices, updateMatrixConway)
  
  # has to be the last thing in this function
  center_window(top)
  top.mainloop()
#


###### Helper Functions ######
def center_window(top):
  # https://stackoverflow.com/a/10018670
  width_screen = top.winfo_screenwidth()
  height_screen = top.winfo_screenheight()
  top.geometry('{}x{}+{}+{}'.format(WIDTH, HEIGHT, (width_screen - WIDTH) // 2, (height_screen - HEIGHT) // 2))
  top.wait_visibility()
  width = top.winfo_width()
  frm_width = top.winfo_rootx() - top.winfo_x()
  win_width = width + 2 * frm_width
  height = top.winfo_height()
  titlebar_height = top.winfo_rooty() - top.winfo_y()
  win_height = height + titlebar_height + frm_width
  x = (width_screen - win_width) // 2
  y = (height_screen - win_height) // 2
  top.geometry('{}x{}+{}+{}'.format(width, height, x, y))
#

def drawGridLines(canvas):
  # see https://docs.python.org/3/library/stdtypes.html#range
  for x_col in range(0, WIDTH, CELL_SIZE):
    canvas.create_line(x_col, 0, x_col, HEIGHT, fill = FG_LINE)
  #
  for y_row in range(0, HEIGHT, CELL_SIZE):
    canvas.create_line(0, y_row, WIDTH, y_row, fill = FG_LINE)
  #
#

def createMatrix():
  # see https://snakify.org/en/lessons/two_dimensional_lists_arrays/#section_2
  return [[False] * COLS for r in range(ROWS)]
#

def updateMatrixOnceDbuf(top, canvas, canvas_cells, matrices, updateFn):
  global GENERATION_COUNT
  GENERATION_COUNT += 1
  updateFn(matrices)
  drawMatrix(top, canvas, canvas_cells, matrices[0])
#

def repeatedlyUpdateMatrixDbuf(top, canvas, canvas_cells, matrices, updateFn):
  def innerUpdate():
    updateMatrixOnceDbuf(top, canvas, canvas_cells, matrices, updateFn)
    top.after(MATRIX_UPDATE_MS, innerUpdate)
  #
  top.after(MATRIX_UPDATE_MS, innerUpdate)
#

def drawMatrix(top, canvas, canvas_cells, matrix):
  # see https://stackoverflow.com/a/12991740
  create = canvas_cells[0][0] == False
  top.title('{} g={}'.format(TITLE, GENERATION_COUNT))
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = matrix[row][col]
      if create:
        x0 = col * CELL_SIZE + 1; x1 = x0 + CELL_SIZE - 1
        y0 = row * CELL_SIZE + 1; y1 = y0 + CELL_SIZE - 1
        canvas_cells[row][col] = canvas.create_polygon(x0, y0, x0, y1, x1, y1, x1, y0)
      #
      cell = canvas_cells[row][col]
      cell_fill = FG_CELL if cell_value else BG_COLOR
      canvas.itemconfig(cell, fill = cell_fill)
    #
  #
#

def printMatrix(matrix):
  print('g={}'.format(GENERATION_COUNT))
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = matrix[row][col]
      ch = 'x' if cell_value else '.'
      print(ch, end=' ')
    #
    print('')
  #
#

def fillMatrixRandomly(matrices):
  for col in range(COLS):
    for row in range(ROWS):
      # see https://stackoverflow.com/a/6824868
      matrices[0][row][col] = (random() < 0.5)
    #
  #
#

NEIGHBOR_CELL_DIFFS = [
  (-1, -1), ( 0, -1), (+1, -1), (+1,  0),
  (+1, +1), ( 0, +1), (-1, +1), (-1,  0)
]
def updateMatrixConway(matrices):
  original_matrix = matrices[0]
  updated_matrix = matrices[1]
  for row in range(ROWS):
    for col in range(COLS):
      live_neighbor_count = 0
      for (dx, dy) in NEIGHBOR_CELL_DIFFS:
        neighbor_col = (col + dx) % COLS
        neighbor_row = (row + dy) % ROWS
        neighbor_value = original_matrix[neighbor_row][neighbor_col]
        live_neighbor_count += 1 if neighbor_value else 0
      #
      original_cell_value = original_matrix[row][col]
      if original_cell_value:
        updated_matrix[row][col] = CONWAY_LIVE_MIN <= live_neighbor_count <= CONWAY_LIVE_MAX
      #
      else:
        updated_matrix[row][col] = CONWAY_BORN_MIN <= live_neighbor_count <= CONWAY_BORN_MAX
      #
    #
  #
  matrices.rotate(1)
#


###### Main Exec ######
if __name__ == '__main__':
  main()
#

