#!/usr/bin/env python3

###### Imports ######
import tkinter as tk
from random import random


###### Constants ######
CELL_SIZE = 25
WIDTH = 800
HEIGHT = int(WIDTH * 9 / 16)
COLS = int(WIDTH / CELL_SIZE)
ROWS = int(HEIGHT / CELL_SIZE)
BG_COLOR = 'blue'
FG_LINE = 'white'
FG_CELL = 'red'


###### Main Method ######
def main():
  # Simple Print
  print("Conway's Game of Life is starting... now.")
  
  # see https://www.tutorialspoint.com/python3/tk_canvas.htm
  top = tk.Tk()
  canvas = tk.Canvas(top, bg = BG_COLOR, width = WIDTH, height = HEIGHT)
  
  drawGridLines(canvas)
  matrix = createMatrix()
  fillMatrixRandomly(matrix)
  drawMatrix(canvas, matrix)
  printMatrix(matrix)
  
  # has to be the last thing in this function
  canvas.pack()
  top.mainloop()
#


###### Helper Functions ######
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

def fillMatrixRandomly(matrix):
  for col in range(COLS):
    for row in range(ROWS):
      # see https://stackoverflow.com/a/6824868
      matrix[row][col] = (random() < 0.5)
    #
  #
#

def drawMatrix(canvas, matrix):
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = matrix[row][col]
      x0 = col * CELL_SIZE + 1; x1 = x0 + CELL_SIZE - 1
      y0 = row * CELL_SIZE + 1; y1 = y0 + CELL_SIZE - 1
      cell_fill = FG_CELL if cell_value else BG_COLOR
      canvas.create_polygon(x0, y0, x0, y1, x1, y1, x1, y0, fill = cell_fill)
    #
  #
#

def printMatrix(matrix):
  for row in range(ROWS):
    for col in range(COLS):
      cell_value = matrix[row][col]
      ch = 'x' if cell_value else '.'
      print(ch, end=' ')
    #
    print('')
  #
#


###### Main Exec ######
if __name__ == '__main__':
  main()
#

