from player import Player
from board import Board

class engine:
    def __init__(self,boardsize,timelimit):
        self.board = Board(boardsize,timelimit)
        
    def terminate_state(self,player):
        if (self.board.boardSize == 8):
            maxIter = 5
        elif (self.board.boardSize == 10):
            maxIter = 6
        else: # default is 16 x 16
            maxIter = 7
        
        if (player == 1):
            print(self.board.player1.goal)
            # for i in range(1, maxIter):
            #     for j in range(1, maxIter):
            #         if (i + j <= maxIter and i < 6 and j < 6):
                        
                        
            
        elif (player == 2):
            print("halo")

# a = Player('WHITE', 10)
# b = Player('BLACK', 10)
# c = Board(16, 10)

# a.printStatus()
# b.printStatus()

# print(a.goal)

e = engine(16,50)
e.terminate_state(1)