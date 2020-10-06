from player import Player
from board import Board

class engine:
    def __init__(self,boardsize,timelimit):
        self.board = Board(boardsize,timelimit)
    
    def terminate_state(self,player):
        player1 = self.board.player1
        player2 = self.board.player2
        
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
        

                        
                        

# a = Player('WHITE', 10)
# b = Player('BLACK', 10)
# # c = Board(16, 10)

# # a.printStatus()
# b.printStatus()

# print(b.goal)

e = engine(16,50)
print(e.terminate_state(2))