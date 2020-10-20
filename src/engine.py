from player import Player
from board import Board
import math
import sys
import re

class Engine:
    def __init__(self, boardsize, timelimit, player, system):
        if (player is not None):
            self.player2 = Player("RED" if player=="GREEN" else "GREEN", boardsize)
            self.player1 = Player(player, boardsize)
            self.selfplay = False
        else:
            self.player1 = Player("RED", boardsize)
            self.player2 = Player("GREEN", boardsize)
            self.selfplay = True
        
        self.board = Board(boardsize, timelimit, self.player1, self.player2, self.selfplay)
        self.turn = 1 #1 for player1, 2 for player2
        # if (system == "GUI"):
            # set gui here
    
    def start(self):
        if (self.selfplay == True):
            while (self.terminate_state() == 0):
                self.board.printBoard()
                print("Turn: ", "PLAYER1" if self.turn == 1 else "PLAYER2")

                if (self.turn == 2):
                    self.board.executeBotMove()
                    inp = input("Press enter to continue ")
                else:
                    self.board.executeBotMove()
                    inp = input("Press enter to continue ")
                
                self.turn = 2 if self.turn == 1 else 1
                self.board.turn = 2 if self.board.turn == 1 else 1
        else:
            while (self.terminate_state() == 0):
                self.board.printBoard()
                player = self.player1 if self.turn == 1 else self.player2
                # print(player.color)
                # bot = self.player2 if self.turn == 1 else self.player1
                # for p in player.pawns:
                #     print(p.x, p.y)
                # print("player goal")
                # for i in player.goal:
                # #     print(i)
                # print(bot.color)
                # for q in bot.pawns:
                #     print(q.x, q.y)
                # print("bot goal")
                # for i in bot.goal:
                #     print(i)
                print("Turn: ", "PLAYER1" if self.turn == 1 else "PLAYER2")

                if (self.turn == 2):
                    self.board.executeBotMove()
                else:
                    chosen = False
                    # player.printStatus()
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
        
        won_player = "Player 1" if self.terminate_state() == 1 else "Player 2"
        print(won_player + " wins the game!")
    
    def terminate_state(self):
        result = None
        if(self.player1.isTerminate() and not(self.player2.isTerminate())):
            result = 1
        elif(self.player2.isTerminate() and not(self.player1.isTerminate())):
            result = 2
        else:
            result = 0 #0 for notterminate
        # print("result is ", result)
        return result

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
    
    if player is not None:
        player = player.upper()
        if player not in ["RED", "GREEN"]:
            print("player should be RED/GREEN")
            exit()
            
    game = Engine(boardsize, timelimit, player, system)
    game.start()