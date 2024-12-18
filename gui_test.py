import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from BFS import BFS

class PuzzleSolverGUI:

    start_button = None
    stop_button = None
    stats_button = None
    previous_button = None
    next_button = None

    def __init__(self, master):
        self.master = master
        master.title("N-Puzzle Solver")
        master.resizable(False, False)  # window unresizable

        # Set window transparency
        master.attributes('-alpha', 0.95)  # for transparency

        # Variables
        self.board_size_var = tk.StringVar(value="3")  # Default size
        self.heuristic_var = tk.StringVar(value="Manhattan")  # Default heuristic function
        self.board_values_var = tk.StringVar(value="2 3 5 1 8 4 0 7 6")  # Default board values
        self.board = None
        self.full_path = None
        self.isStopped = False
        self.current_state = None

        # Initialize GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Some styling for buttons
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", borderwidth=0, font=('Helvetica', 12))
        style.map("TButton",
                background=[('pressed', '#0056b3'), ('active', '#007bff')],
                foreground=[('pressed', 'white'), ('active', 'white')],
                relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

        # Main Frame
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.grid(row=0, column=0)

        # Board Size Dropdown
        board_size_label = ttk.Label(main_frame, text="Board Size:", font=('Helvetica', 12))
        board_size_label.grid(row=0, column=0, padx=5, pady=5)

        board_size_options = ["3", "4", "5"]  # board size
        board_size_dropdown = ttk.Combobox(main_frame, textvariable=self.board_size_var, values=board_size_options, state="readonly")
        board_size_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Heuristic Function Dropdown
        heuristic_label = ttk.Label(main_frame, text="Heuristic Function:", font=('Helvetica', 12))
        heuristic_label.grid(row=1, column=0, padx=5, pady=5)

        heuristic_options = ["Manhattan", "Hamming", "Euclidean", "Linear_Conflict"]  # Add more heuristics if needed
        heuristic_dropdown = ttk.Combobox(main_frame, textvariable=self.heuristic_var, values=heuristic_options, state="readonly")
        heuristic_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Text Entry for Board Values
        board_values_label = ttk.Label(main_frame, text="Enter Board (space-separated EX: 1 2 3 ...): \n* 0 indicates empty box", font=('Helvetica', 10))
        board_values_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        board_values_entry = ttk.Entry(main_frame, textvariable=self.board_values_var, font=('Helvetica', 12))
        board_values_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Set Button
        self.set_button = ttk.Button(button_frame, text="Set", command=self.set_solver, style="TButton")
        self.set_button.grid(row=0, column=0, padx=5)

        # Start Button
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_solver, style="TButton")
        self.start_button.grid(row=0, column=1, padx=5)

        # Stop Button
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_solver, style="TButton")
        self.stop_button.grid(row=0, column=2, padx=5)

        # Get Stats
        self.stats_button = ttk.Button(button_frame, text="Stats", command=self.get_states, style="TButton")
        self.stats_button.grid(row=0, column=3, padx=5)

        # Previous and Next Buttons
        self.previous_button = ttk.Button(button_frame, text="◀", width=3, command=self.previous_state)
        self.previous_button.grid(row=0, column=4, padx=5)

        self.next_button = ttk.Button(button_frame, text="▶", width=3, command=self.next_state)
        self.next_button.grid(row=0, column=5, padx=5)

        # Puzzle Board
        self.puzzle_board = tk.Canvas(main_frame, width=400, height=400, bg="#eaeaea", borderwidth=0, highlightthickness=0)
        self.puzzle_board.grid(row=5, column=0, columnspan=6, pady=10)

        # Initial board
        self.update_board([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        self.stats_button["state"] = "disabled"
        self.previous_button["state"] = "disabled"
        self.next_button["state"] = "disabled"

    def update_board(self, values):
        # Update the board based on the updated values from logic
        size = int(self.board_size_var.get())

        if len(values) == size * size:
            self.draw_board(size, values)

    def draw_board(self, size, values):
        # Clear the existing board
        self.puzzle_board.delete("all")

        # Calculate cell size based on the board size
        cell_size = 400 // size
        static_color = "#EFC3CA"  # Set your desired static color here
        for i in range(size):
            for j in range(size):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size

                # Draw a rectangle for each cell with the static color
                self.puzzle_board.create_rectangle(x1, y1, x2, y2, outline="black", fill=static_color)

                # Add numbers to the cells (skip for the last cell)
                number = ''
                if values[i * size + j] != 0:
                    number = values[i * size + j]
                text_color = "gray29"
                # Increase the font size of the numbers
                font_size = int(cell_size // 2)
                self.puzzle_board.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(number), fill=text_color,
                                            font=('Helvetica', font_size, 'bold'))

    def start_solver(self):
        self.stop_button["state"] = "normal"
        self.start_button["state"] = "disabled"
        self.set_button["state"] = "disabled"
        self.isStopped = False
        heuristic_function = self.heuristic_var.get()
        heu_index = self.getHeuIndex(heuristic_function)
        print(f"Starting solver with heuristic function: {heuristic_function}")
        if self.board is not None:
            self.full_path = self.board.solve(heu_index)
            if self.full_path != -1:
                self.print_path()
                self.current_state = self.board.getMoves()
                if self.isStopped:
                    messagebox.showerror("Stop Solve", "Process is Stopped.")
                else:
                    self.get_solution_info()
                    self.set_button["state"] = "normal"
                    self.previous_button["state"] = "normal"
                    self.next_button["state"] = "normal"
                    self.stop_button["state"] = "disabled"
                    self.start_button["state"] = "disabled"
            else:
                messagebox.showerror("Error", "No Solution for this Board or Search time exceeded")
                self.set_button["state"] = "normal"
                self.start_button["state"] = "disabled"
                self.stop_button["state"] = "disabled"
                self.stats_button["state"] = "disabled"
                self.previous_button["state"] = "disabled"
                self.next_button["state"] = "disabled"

    def set_solver(self):
        size = int(self.board_size_var.get())
        values_str = self.board_values_var.get()
        values = [int(val) for val in values_str.split() if val.isdigit()]
        if len(values) == size * size:
            board2d = self.convert_to_2d_array(values)
            if BFS.isValid(board2d):
                self.draw_board(size, values)
                self.board = BFS(board2d)
                self.current_state = None
                self.start_button["state"] = "normal"
                self.stats_button["state"] = "normal"
            else:
                messagebox.showerror("Wrong", "Check the input please!")
                self.start_button["state"] = "disabled"
                self.stop_button["state"] = "disabled"
                self.stats_button["state"] = "disabled"
                self.previous_button["state"] = "disabled"
                self.next_button["state"] = "disabled"
        else:
            messagebox.showerror("Wrong", "Check the input please!")
            self.start_button["state"] = "disabled"
            self.stop_button["state"] = "disabled"
            self.stats_button["state"] = "disabled"
            self.previous_button["state"] = "disabled"
            self.next_button["state"] = "disabled"

    def stop_solver(self):
        self.isStopped = True
        print("Solver stopped.")
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        self.stats_button["state"] = "disabled"
        self.previous_button["state"] = "disabled"
        self.next_button["state"] = "disabled"
        self.set_button["state"] = "normal"

    def print_path(self):
        for state in self.full_path:
            if self.isStopped:
                return
            state1d = self.convert_to_1d_array(state)
            self.update_board(state1d)
            self.master.update()  # Update the GUI immediately
            self.master.after(500)  # Delay for 500 milliseconds

    def getHeuIndex(self, name):
        heu = ["Manhattan", "Hamming", "Euclidean", "Linear_Conflict"]
        for n in heu:
            if n == name:
                return heu.index(n)

    def get_solution_info(self):
        messagebox.showinfo(f"Game is Solved ({self.heuristic_var.get()})", 
                            f"Number of Visited Nodes: {self.board.getNumOfSteps()}\n"
                            f"Number of Moves: {self.board.getMoves()}\n"
                            f"Time: {self.board.getTime()}")

    def get_states(self):
        if self.board is not None:
            initial = self.board.get_initial()
            all = [BFS(initial), BFS(initial), BFS(initial), BFS(initial)]
            heu = ["Manhattan", "Hamming", "Euclidean", "Linear_Conflict"]
            msg = "Number of Visited Nodes:\n"
            msg1 = "Number of Moves:\n"
            x = []
            y = []
            times = []
            i = 0
            for h in all:
                result = h.solve(i)
                if result != -1:
                    steps = h.getNumOfSteps()
                    moves = h.getMoves()
                    msg += f"{heu[i]}: {steps}\n"
                    msg1 += f"{heu[i]}: {moves}\n"
                    x.append(heu[i])
                    times.append(round(h.getTime(), 2))
                    y.append(h.getNumOfSteps())
                    i += 1
                else:
                    break
            if result != -1:
                BFS.getGraph(x, y, times)
                messagebox.showinfo("Game is Solved", msg + '\n' + msg1)
            else:
                messagebox.showerror("Error", "No Solution for this Board or Search time exceeded")

    def next_state(self):
        if self.current_state is not None:
            if self.current_state < self.board.getMoves():
                self.current_state += 1
                state = self.full_path[self.current_state]
                board1d = self.convert_to_1d_array(state)
                self.update_board(board1d)

    def previous_state(self):
        if self.current_state is not None:
            if self.current_state > 0:
                self.current_state -= 1
                state = self.full_path[self.current_state]
                board1d = self.convert_to_1d_array(state)
                self.update_board(board1d)

    def convert_to_2d_array(self, arr_1d):
        n = int(math.sqrt(len(arr_1d)))

        if n * n != len(arr_1d):
            raise ValueError("Input array size must be a perfect square.")

        return [arr_1d[i:i + n] for i in range(0, len(arr_1d), n)]

    def convert_to_1d_array(self, matrix):
        return [element for row in matrix for element in row]
