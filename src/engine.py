from player import Player
from board import Board
import math
import sys

class Engine:
    def __init__(self, boardsize, timelimit, player, system):
        # if (player == "GREEN"):
        #     bot = "RED"
        # elif (player == "RED"):
        #     bot = "GREEN"
        # else:
        #     player = "GREEN"
        #     bot = "RED"
        #     self.selfplay = True
        
        self.board = Board(boardsize,timelimit, player, system)
    
    # def start(self):
    #     while (self.terminate_state() == 0):
    #         self.board.printBoard()
    #         print("Turn: ", turn)
    #         print("Available moves: ", available_moves)
    #         to_x, to_y = tuple(input("Where do you want to move? [Write in (x,y)]"))
    #         print("Executing moves...")
    #         execute_moves()
    #         print()

    #         turn = "RED" if self.turn == "GREEN" else "RED"
        
    #     won_player = "Player 1" if self.terminate_state() == 1 else "Player 2"
    #     print(won_player + " wins the game!")
    
    def terminate_state(self,player):
        self.player1 = self.board.player1
        self.player2 = self.board.player2
        if(player1.isTerminate() and not(player2.isTerminate())):
            result = 1
        elif(player2.isTerminate() and not(player1.isTerminate())):
            result = -1
        else:
            result = 0 #0 for notterminate
        #for player2
        if(player == 2):
            result *= -1
        return result
        

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python engine.py <boardsize> <timelimit> <gamesystem> [player]")
        print("boardsize: 8, 10, 16")
        print("player: RED/GREEN")
        print("gamesystem: CMD/GUI")
        exit()

    boardsize, timelimit, system = sys.argv[1:4]
    player = sys.argv[4] if len(sys.argv) == 5 else None

    if boardsize not in ("8", "10", "16"):
        print("boardsize should be 8, 10, or 16")
        exit()    

    if not boardsize.isdigit() or not timelimit.isdigit():
        print("boardsize and timelimit should be integer")
        exit()

    boardsize = int(boardsize)
    timelimit = int(timelimit)
    system = system.upper()

    if (system not in ("CMD", "GUI")):
        print("gamesystem should be CMD/GUI")
    
    if player is not None:
        player = player.upper()

    if player not in ("RED", "GREEN"):
        print("player should be RED/GREEN")
        exit()
            
    game = Engine(boardsize, timelimit, player, system)