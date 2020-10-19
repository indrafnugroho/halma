from player import Player
from board import Board
import math
import sys
import re

class Engine:
    def __init__(self, boardsize, timelimit, player, system):
        self.bot = Player("RED" if player=="GREEN" else "GREEN", boardsize)
        self.player = Player(player, boardsize)
        # elif (player == "RED"):
        #     self.bot = Player("GREEN", boardsize)
        #     self.player = Player("RED", boardsize)
        # else:
        #     self.bot = Player("RED", boardsize)
        #     self.player = Player("GREEN", boardsize)
        #     self.selfplay = True
        
        self.board = Board(boardsize, timelimit, self.player, self.bot)
        self.turn = 1 #1 for player, 2 for bot
    
    def start(self):
        while (self.terminate_state() == 0):
            self.board.printBoard()
            player = self.player if self.turn == 1 else self.bot
            # print(player.color)
            bot = self.bot if self.turn == 2 else self.player
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
            print("Turn: ", "PLAYER" if self.turn == 1 else "BOT")

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
                        print("Pawn not available! Available pawns : ", pawns)
                    else:
                        chosen = True


            moved = False
            while not(moved):
                print("Available moves: ", self.board.getMoveFromTile(player, fromx, fromy))
                to_x, to_y = input("Where do you want to move? Write in [x,y] without [] ").split(",")
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
        if(self.player.isTerminate() and not(self.bot.isTerminate())):
            result = 1
        elif(self.bot.isTerminate() and not(self.player.isTerminate())):
            result = 2
        else:
            result = 0 #0 for notterminate
        print("result is ", result)
        return result

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python engine.py <boardsize> <timelimit> <gamesystem> [player]")
        print("boardsize: 8, 10, 16")
        print("(timelimt: any number in second)")
        print("player: RED/GREEN")
        print("gamesystem: CMD/GUI")
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