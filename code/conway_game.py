#!/usr/bin/env python3

###### Imports ######
import tkinter as tk
from tkinter import N, S, E, W
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
class VariableState(object): pass


###### Main Method ######
def main():
  state = VariableState()
  state.generation_count = 0
  
  # see https://www.tutorialspoint.com/python3/tk_canvas.htm
  state.root = tk.Tk()
  state.root.title(TITLE)
  state.canvas = tk.Canvas(state.root, bg = BG_COLOR, width = WIDTH, height = HEIGHT)
  state.canvas_cells = createMatrix()
  drawGridLines(state.canvas)
  
  # labels
  state.label_gen = tk.Label(state.root, text = 'label')
  
  # see https://effbot.org/tkinterbook/button.htm
  def button_pause__click():
    print('pause clicked!')
  #
  state.button_pause = tk.Button(state.root, text = 'Pause', command = button_pause__click)
  
  # see https://effbot.org/tkinterbook/grid.htm
  state.canvas.grid(row = 0, column = 0, columnspan = 2, sticky = N+S+E+W)
  state.button_pause.grid(row = 1, column = 0, sticky = N+S+E+W)
  state.label_gen.grid(row = 1, column = 1, sticky = E)
  
  # see https://stackoverflow.com/a/9457884
  state.matrices = deque([createMatrix(), createMatrix()])
  
  # see https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)
  state.matrices[0][1+5][2] = True
  state.matrices[0][2+5][3] = True
  state.matrices[0][3+5][1] = True
  state.matrices[0][3+5][2] = True
  state.matrices[0][3+5][3] = True
  
  drawMatrix(state)
  repeatedlyUpdateMatrixDbuf(state, updateMatrixConway)
  
  # has to be the last thing in this function
  center_window(state.root)
  state.root.mainloop()
#


###### Helper Functions ######
def center_window(root):
  # https://stackoverflow.com/a/10018670
  width_screen = root.winfo_screenwidth()
  height_screen = root.winfo_screenheight()
  root.geometry('+{}+{}'.format(
    (width_screen - WIDTH) // 2,
    (height_screen - HEIGHT) // 2
  ))
  root.wait_visibility()
  width = root.winfo_width()
  frm_width = root.winfo_rootx() - root.winfo_x()
  win_width = width + 2 * frm_width
  height = root.winfo_height()
  titlebar_height = root.winfo_rooty() - root.winfo_y()
  win_height = height + titlebar_height + frm_width
  x = (width_screen - win_width) // 2
  y = (height_screen - win_height) // 2
  root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
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

def updateMatrixOnceDbuf(state, updateFn):
  state.generation_count += 1
  updateFn(state)
  drawMatrix(state)
#

def repeatedlyUpdateMatrixDbuf(state, updateFn):
  def innerUpdate():
    updateMatrixOnceDbuf(state, updateFn)
    state.root.after(MATRIX_UPDATE_MS, innerUpdate)
  #
  state.root.after(MATRIX_UPDATE_MS, innerUpdate)
#

def drawMatrix(state):
  # see https://stackoverflow.com/a/12991740
  create = state.canvas_cells[0][0] == False
  state.label_gen.config(text = 'g=%s' % (state.generation_count))
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = state.matrices[0][row][col]
      if create:
        x0 = col * CELL_SIZE + 1; x1 = x0 + CELL_SIZE - 1
        y0 = row * CELL_SIZE + 1; y1 = y0 + CELL_SIZE - 1
        state.canvas_cells[row][col] = state.canvas.create_polygon(x0, y0, x0, y1, x1, y1, x1, y0)
      #
      cell = state.canvas_cells[row][col]
      cell_fill = FG_CELL if cell_value else BG_COLOR
      state.canvas.itemconfig(cell, fill = cell_fill)
    #
  #
#

def printMatrix(matrix):
  print('g={}'.format(Vars.GENERATION_COUNT))
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = matrix[row][col]
      ch = 'x' if cell_value else '.'
      print(ch, end=' ')
    #
    print('')
  #
#


###### Update Functions ######
def updateMatrixRandomly(state):
  for col in range(COLS):
    for row in range(ROWS):
      # see https://stackoverflow.com/a/6824868
      state.matrices[0][row][col] = (random() < 0.5)
    #
  #
#

NEIGHBOR_CELL_DIFFS = [
  (-1, -1), ( 0, -1), (+1, -1), (+1,  0),
  (+1, +1), ( 0, +1), (-1, +1), (-1,  0)
]
def updateMatrixConway(state):
  original_matrix = state.matrices[0]
  updated_matrix = state.matrices[1]
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
  state.matrices.rotate(1)
#


###### Main Exec ######
if __name__ == '__main__':
  main()
#

