#!/usr/bin/env python3

# see https://stackoverflow.com/questions/17843596/difference-between-tkinter-and-tkinter
# and https://python-future.org/compatible_idioms.html#tkinter
import tkinter as tk

###### Main Method ######
def main():
  # Simple Print
  print("Conway's Game of Life is starting... now.")
  
  # see https://www.tutorialspoint.com/python3/tk_canvas.htm
  top = tk.Tk()
  canvas = tk.Canvas(top, bg = "blue", width = 800, height = 450)
  arc = canvas.create_arc((10, 50, 240, 210), start = 0, extent = 150, fill = "red")
  line = canvas.create_line(10, 10, 200, 200, fill = 'white')
  canvas.pack()
  top.mainloop()
#



###### Main Exec ######
if __name__ == '__main__':
  main()
#

