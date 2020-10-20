from player import Player
from board import Board
from coordinate import Coordinate
import tkinter as tk
import math
import sys
import re
import time
from multiprocessing import Process
import time

class Engine:
    def __init__(self, boardsize, timelimit, player, system, bot):
        if (player is not None):
            self.player2 = Player("RED" if player=="GREEN" else "GREEN", boardsize)
            self.player1 = Player(player, boardsize)
            self.selfplay = False
        else:
            self.player1 = Player("RED", boardsize)
            self.player2 = Player("GREEN", boardsize)
            self.selfplay = True
        
        self.board = Board(boardsize, timelimit, self.player1, self.player2, self.selfplay, bot) 
        self.turn = 1 #1 for player, 2 for bot
        self.bot = bot
        self.timelimit = self.board.timelimit
        self.timePlayer1 = 0
        self.timePlayer2 = 0
        if (system == "GUI"):
            self.system = "GUI"
        else:
            self.system = "CMD"
        self.start()
    
    def start(self):
        if (self.selfplay == True):
            if (self.system == "CMD"):
                # BOT VS BOT CMD MODE
                start = time.time()
                while (self.terminate_state() == 0):
                    self.board.printBoard()
                    print("Turn: ", "PLAYER1" if self.turn == 1 else "PLAYER2")

                    start_time = time.time()
                    p = Process(target=self.board.executeBotMove())
                    p.start()
                    p.join(timeout=self.timelimit)

                    if p.is_alive():
                        # If bot is still running
                        p.terminate()
                        print('Bot exceed time limit!')
                        
                    end_time = time.time()
                    time_taken = end_time - start_time

                    print("Time taken for bot", self.turn, ":", time_taken)

                    if (self.turn == 1):
                        self.timePlayer1 += time_taken
                    else:
                        self.timePlayer2 += time_taken
                    
                    # inp = input("Press enter to continue ")
                    
                    self.turn = 2 if self.turn == 1 else 1
                    self.board.turn = 2 if self.board.turn == 1 else 1
                end = time.time()
                print("Execution time:", end - start)
            else:
                # BOT VS BOT GUI MODE
                start = time.time()
                self.gui = BoardGUI(self.board)
                # self.gui.mainloop()
                while (self.terminate_state() == 0):
                    self.gui.drawPawn()
                    if (self.turn == 2):
                        self.board.executeBotMove()
                    else:
                        self.board.executeBotMove()
                    self.turn = 2 if self.turn == 1 else 1
                    self.board.turn = 2 if self.board.turn == 1 else 1
                end = time.time()
                print("Execution time:", end - start)
                
        else:
            # BOT VS USER GUI MODE
            if (self.system == "CMD"):
                start = time.time()
                while (self.terminate_state() == 0):
                    self.board.printBoard()
                    player = self.player1 if self.turn == 1 else self.player2
                    print("Turn: ", "PLAYER1" if self.turn == 1 else "PLAYER2")

                    if (self.turn == 2):
                        start_time = time.time()
                        p = Process(target=self.board.executeBotMove())
                        p.start()
                        p.join(timeout=self.timelimit)

                        if p.is_alive():
                            # If bot is still running
                            p.terminate()
                            print('Bot exceed time limit!')

                        end_time = time.time()
                        time_taken = end_time - start_time

                        print("Time taken for bot", self.turn, ":", time_taken)

                        self.timePlayer2 += time_taken
                            
                    else:
                        if (self.system == "CMD"):
                            chosen = False
                            while (not(chosen)):
                                pawn = input("Choose your pawn. Write in [x,y] without [] ")
                            
                                if not(re.search("[0-9][,][0-9]", pawn) == None):
                                    fromx, fromy = pawn.split(",")
                                    fromx = int(fromx)
                                    fromy = int(fromy)
                                    if (not(player.isExist_pawns(fromx, fromy))):
                                        pawns = ''
                                        for i in range (len(player.pawns)):
                                            pawns += "(" + str(player.pawns[i].x) + "," + str(player.pawns[i].y) + ") "
                                        print("Pawn not available in current coordinate! Available pawns :", pawns)
                                    elif (len(self.board.getMoveFromTile(player, fromx, fromy)) == 0):
                                        pawns = ''
                                        for i in range (len(player.pawns)):
                                            if (player.pawns[i].x != fromx and player.pawns[i].y != fromy):
                                                pawns += "(" + str(player.pawns[i].x) + "," + str(player.pawns[i].y) + ") "
                                        print("No move available, please choose other pawn! Available pawns :", pawns)
                                    else:
                                        chosen = True

                            moved = False
                            while not(moved):
                                print("Available moves: ", self.board.getMoveFromTile(player, fromx, fromy))
                                move = input("Where do you want to move? Write in [x,y] without [] ")
                                
                                if (not(re.search("[0-9][,][0-9]", move) == None)):
                                    to_x, to_y = move.split(",")
                                    to_x = int(to_x)
                                    to_y = int(to_y)
                                    if ((to_x, to_y) in self.board.getMoveFromTile(player, fromx, fromy)):
                                        print("Executing moves...")
                                        self.board.movePawn((fromy, fromx), (to_y, to_x))
                                        print()
                                        moved = True
                                    else:
                                        print("Invalid move!")

                    self.turn = 2 if self.turn == 1 else 1
                end = time.time()
                print("Execution time:", end - start)
            else:
                # BOT VS USER GUI MODE
                start = time.time()
                self.gui = BoardGUI(self.board)
                # self.gui.mainloop()
                self.gui.move = True
                while (self.terminate_state() == 0):
                    if (self.turn == 2 and not(self.gui.move)):
                        self.board.executeBotMove()
                        self.gui.drawPawn()
                        self.gui.move = True
                    else:
                        self.gui.drawPawn()
                        # self.gui.move = False
                    self.turn = 2 if self.turn == 1 else 1
                    self.board.turn = 2 if self.board.turn == 1 else 1
                end = time.time()
                print("Execution time:", end - start)
                    

        won_player = "Player 1" if self.terminate_state() == 1 else "Player 2"
        print(won_player + " wins the game!")
        if not self.selfplay:
            print('Total time for bot:', self.timePlayer2)
        else:
            print('Total time for bot 1:', self.timePlayer1)
            print('Total time for bot 2:', self.timePlayer2)

    def terminate_state(self):
        result = None
        if(self.player1.isTerminate() and not(self.player2.isTerminate())):
            result = 1
        elif(self.player2.isTerminate() and not(self.player1.isTerminate())):
            result = 2
        else:
            result = 0 #0 for notterminate
        return result


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
        self.board.selected_tuple= None
    
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
                self.tiles[col,row] = tile
                self.canvas.tag_bind(tile, "<1>", lambda event, row=row, col=col: self.clicked(row+1, col+1))

        self.drawPawn()

    def drawPawn(self):
        canvas_width = 600
        canvas_height = 600
        border_size = 10
        cell = int(canvas_height / self.board_size)
        self.player1Pawn = self.board.player1.pawns
        self.player2Pawn = self.board.player2.pawns
        # delete previous pawns canvas
        self.canvas.delete('pawn')

        for i in range(len(self.player1Pawn)):
            col = self.player1Pawn[i].x - 1
            row = self.player1Pawn[i].y - 1 
            x1 = col * cell + border_size / 2
            y1 = row * cell + border_size / 2
            x2 = (col + 1) * cell - border_size / 2
            y2 = (row + 1) * cell - border_size / 2
            if (self.board.player1.color == "GREEN"):
                pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#67BF9B")
            else:
                pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#CF6E67")
            self.canvas.tag_bind(pawn, "<1>", lambda event, row=row, col=col: self.clicked(row+1, col+1))

        for i in range(len(self.player2Pawn)):
            col = self.player2Pawn[i].x - 1
            row = self.player2Pawn[i].y - 1 
            x1 = col * cell + border_size / 2
            y1 = row * cell + border_size / 2
            x2 = (col + 1) * cell - border_size / 2
            y2 = (row + 1) * cell - border_size / 2
            if (self.board.player1.color == "GREEN"):
                pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#CF6E67")
            else:
                pawn = self.canvas.create_oval(x1, y1, x2, y2, tags="pawn", width=0, fill="#67BF9B")
            self.canvas.tag_bind(pawn, "<1>")

        # update pawn's coordinate everytime it moves
        self.update()

    def clicked(self, row, column):
        tile = self.tiles[column -1, row-1]
        toBeBordered = []
        toBeBordered.append(tile)
        if (self.board.selected_tuple == None and self.board.player1.isExist_pawns(column, row)):
            if (self.board.player1.isExist_pawns(column, row)):
                pawn = self.board.player1.getPawn(column, row)
            elif (self.board.player2.isExist_pawns(column, row)):
                pawn = self.board.player2.getPawn(column, row)

            validMoves = self.board.getAksiValid(pawn)

            for i in range (len(validMoves)):
                (x, y) = validMoves[i]
                tile = self.tiles[x-1, y-1]
                toBeBordered.append(tile)

            for i in range (len(toBeBordered)):
                self.canvas.itemconfigure(toBeBordered[i], outline="black", width = 2)

            self.board.selected_tuple = (column, row)

        elif (self.board.selected_tuple != None and (column, row) in self.board.getAksiValid(self.board.player1.getPawn(self.board.selected_tuple[0], self.board.selected_tuple[1]))):
            (x,y) = self.board.selected_tuple
            self.board.movePawn((y, x), (row, column))
            for i in range (self.board_size):
                for j in range (self.board_size):
                    self.canvas.itemconfigure(self.tiles[i,j], outline="black", width = 0)
            self.board.selected_tuple = None
            self.move = False
        else:
            self.board.selected_tuple = None
            for i in range (self.board_size):
                for j in range (self.board_size):
                    self.canvas.itemconfigure(self.tiles[i,j], outline="black", width = 0)
        self.update()



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python engine.py <boardsize> <timelimit> <gamesystem> [player]")
        print("boardsize: 8, 10, 16")
        print("timelimit: any number in second")
        print("gamesystem: CMD/GUI")
        print("player: RED/GREEN")
        exit()

    boardsize, timelimit, system = sys.argv[1:4]
    player = sys.argv[4] if len(sys.argv) == 5 else None

    if boardsize not in ["8", "10", "16"]:
        print("boardsize should be 8, 10, or 16")
        exit()    

    if not boardsize.isdigit() or not timelimit.isdigit():
        print("boardsize and timelimit should be integer")
        exit()

    boardsize = int(boardsize)
    timelimit = int(timelimit)
    system = system.upper()

    if (system not in ["CMD", "GUI"]):
        print("gamesystem should be CMD/GUI")
    
    bot = None
    if player is not None:
        player = player.upper()
        if player not in ["RED", "GREEN"]:
            print("player should be RED/GREEN")
            exit()
        print("What bot do you want to fight? [Minimax/MinimaxLocalSearch]")
        bot = input("Write the abbreviation of choices above [M/MLS]: ")

        bot = bot.upper()
        if bot not in ["M", "MLS"]:
            print("bot should be M/MLS")
            exit()
    
    game = Engine(boardsize, timelimit, player, system, bot)