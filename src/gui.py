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
        
        self.tiles = {}

        # grid canvas
        # showing white blank canvas with size 600*600
        self.canvas = tk.Canvas(self, width=600, height=600, bg="#fff", highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=self.board_size, rowspan=self.board_size)

        self.columnconfigure(0, minsize=50)
        self.rowconfigure(0, minsize=50)
        self.columnconfigure(self.board_size + 1, minsize=50)
        self.rowconfigure(self.board_size + 1, minsize=50)
        self.canvas.bind("<Configure>", self.drawTiles)
    
    def drawTiles(self, event=None):
        self.canvas.delete("tile")
        canvas_width = 600
        canvas_height = 600
        border_size = 1
        cell = int(canvas_height / self.board_size)
        for col in range (self.board_size):
            for row in range (self.board_size):
                x1 = col * cell + border_size / 2
                y1 = row * cell + border_size / 2
                x2 = (col + 1) * cell - border_size / 2
                y2 = (row + 1) * cell - border_size / 2

                if (self.board_size == 8):
                    player1 = 4
                    player2 = 10
                elif (self.board_size == 10):
                    player1 = 5
                    player2 = 13
                else:
                    player1 = 6
                    player2 = 24

                if ((row + col) < player1):
                    if ((row + col) % 2 == 0):
                        color = '#AC352E'
                    else:
                        color = '#D0352E'
                elif ((row + col ) > player2):
                    if ((row + col) % 2 == 0):
                        color = '#12C47A'
                    else:
                        color = '#0FA868'
                else:
                    if ((row + col) % 2 == 0):
                        color = '#ECCB96'
                    else:
                        color = '#BAA077'
                tile = self.canvas.create_rectangle(x1, y1, x2, y2, tags="tile", width=0, fill=color)
                self.tiles[row,col] = tile
                self.canvas.tag_bind(tile, "<1>")

        self.drawPawn()

    def clicked(self, row, column):
        toBeBordered = []
        tile = self.tiles[row -1, column-1]
        toBeBordered.append(tile)
        border = int(float(self.canvas.itemcget(tile, "width")))
        if border == 0:
            border = 2
            for i in range (self.board_size):
                for j in range (self.board_size):
                    if (i == row-1 and j == column-1):
                        self.canvas.itemconfigure(self.tiles[i,j], outline="black", width = 1)
                    else:
                        self.canvas.itemconfigure(self.tiles[i,j], outline="black", width = 0)
            if (self.board.player1.isExist_pawns(row, column)):
                pawn = self.board.player1.getPawn(row, column)
            elif (self.board.player2.isExist_pawns(row, column)):
                pawn = self.board.player2.getPawn(row, column)
            validMoves = self.board.getAksiValid(pawn)
            print("valid moves = ", validMoves)
            for i in range (len(validMoves)):
                (x, y) = validMoves[i]
                tile = self.tiles[x-1, y-1]
                toBeBordered.append(tile)
        else:
            for i in range (self.board_size):
                for j in range (self.board_size):
                    self.canvas.itemconfigure(self.tiles[i,j], outline="black", width = 0)
        
        for i in range (len(toBeBordered)):
            self.canvas.itemconfigure(toBeBordered[i], outline="black", width = border)

    def drawPawn(self):
        canvas_width = 600
        canvas_height = 600
        border_size = 10
        cell = int(canvas_height / self.board_size)
        player1Pawn = self.board.player1.pawns
        player2Pawn = self.board.player2.pawns
        # self.board.player1.printStatus()
        # self.board.player2.printStatus()

        # delete previous pawns canvas
        self.canvas.delete('pawn')

        for i in range(len(player1Pawn)):
            col = player1Pawn[i].x - 1
            row = player1Pawn[i].y - 1 
            x1 = col * cell + border_size / 2
            y1 = row * cell + border_size / 2
            x2 = (col + 1) * cell - border_size / 2
            y2 = (row + 1) * cell - border_size / 2
            # print("pion player 1 ke-" + str(i) + " col = " + str(col) + " row = " + str(row))
            pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#CF6E67")
            self.canvas.tag_bind(pawn, "<1>", lambda event, row=row, col=col: self.clicked(row+1, col+1))

        for i in range(len(player2Pawn)):
            col = player2Pawn[i].x - 1
            row = player2Pawn[i].y - 1 
            x1 = col * cell + border_size / 2
            y1 = row * cell + border_size / 2
            x2 = (col + 1) * cell - border_size / 2
            y2 = (row + 1) * cell - border_size / 2
            # print("pion player 2 ke-" + str(i) + " col = " + str(col) + " row = " + str(row))
            pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#67BF9B")
            self.canvas.tag_bind(pawn, "<1>", lambda event, row=row, col=col: self.clicked(row+1, col+1))

        # update pawn's coordinate everytime it moves
        self.update()


# if __name__ == '__main__':
#     board = Board(8, 100, "GREEN", "GUI")
#     gui = BoardGUI(board)
#     gui.mainloop()