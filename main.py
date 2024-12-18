import tkinter as tk
from gui_test import PuzzleSolverGUI

# 8-Puzzle
# (Goal) 1 2 3 4 5 6 7 8 0
#        2 3 5 1 8 4 0 7 6
#        1 0 3 5 2 6 4 7 8
#        1 0 3 6 2 7 4 5 8 

# 15-Puzzle
# (Goal) 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
#        1 6 2 4 10 5 3 8 11 7 14 12 9 13 0 15

# 24-Puzzle
# (Goal) 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 0
#        1 2 3 4 5 6 7 9 0 10 11 13 8 14 15 17 12 18 19 20 16 21 22 23 24

root = tk.Tk()
app = PuzzleSolverGUI(root)
root.mainloop()

