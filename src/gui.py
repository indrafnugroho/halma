import tkinter as tk
from board import Board 

# class BoardGUI that is derived from tk.Tk parent class
class BoardGUI(tk.Tk):
    def __init__(self, board, *args, **kwargs):
        # initialize parent tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # metadata
        self.title('Halma')
        self.resizable(True, True)
        self.configure(bg='#fff')

        # variables
        self.board = board
        self.board_size = board.getSize()

        # row and column labels
        # showing number row labels and char column labels
        for i in range(self.board_size):
            row_label = tk.Label(self, text=i+1, font='Times', bg='#fff', fg='#000')
            row_label.grid(row=i+1, column=0)

            col_label = tk.Label(self, text=chr(i+97), font='Times', bg='#fff', fg='#000')
            col_label.grid(row=0, column=i+1)

        # grid canvas
        # showing white blank canvas with size 600*600
        self.canvas = tk.Canvas(self, width=600, height=600, bg="#fff", highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=self.board_size, rowspan=self.board_size)

        self.columnconfigure(0, minsize=50)
        self.rowconfigure(0, minsize=50)
        self.columnconfigure(self.board_size + 1, minsize=50)
        self.rowconfigure(self.board_size + 1, minsize=50)

if __name__ == '__main__':
    board = Board(16,3)
    gui = BoardGUI(board)
    gui.mainloop()