#!/usr/bin/env python3

###### Imports ######
import tkinter as tk


###### Constants ######
CELL_SIZE = 25
WIDTH = 800
HEIGHT = int(WIDTH * 9 / 16)
COLS = int(WIDTH / CELL_SIZE)
ROWS = int(HEIGHT / CELL_SIZE)
BG_COLOR = 'blue'
FG_LINE = 'white'


###### Main Method ######
def main():
  # Simple Print
  print("Conway's Game of Life is starting... now.")
  
  # see https://www.tutorialspoint.com/python3/tk_canvas.htm
  top = tk.Tk()
  canvas = tk.Canvas(top, bg = BG_COLOR, width = WIDTH, height = HEIGHT)
  
  # see https://docs.python.org/3/library/stdtypes.html#range
  for x_col in range(0, WIDTH, CELL_SIZE):
    canvas.create_line(x_col, 0, x_col, HEIGHT, fill = FG_LINE)
  #
  for y_row in range(0, HEIGHT, CELL_SIZE):
    canvas.create_line(0, y_row, WIDTH, y_row, fill = FG_LINE)
  #
  
  # has to be the last thing in this function
  canvas.pack()
  top.mainloop()
#


###### Main Exec ######
if __name__ == '__main__':
  main()
#

