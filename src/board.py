from player import Player

class Board:
  def __init__(self, boardSize, timeLimit):
    self.boardSize = boardSize
    self.player1 = Player('WHITE', boardSize)
    self.player2 = Player('BLACK', boardSize)
    self.turn = self.player1

  def printBoard(self):
    tempPosisiPion = []
    for pawn in self.player1.pawns:
      tempPosisiPion.append((pawn.x, pawn.y))
    for pawn in self.player2.pawns:
      tempPosisiPion.append((pawn.x, pawn.y))
    tempPosisiPion.sort()
  
  def getSize(self):
    return self.boardSize
  
  def isEmpty(self,x,y):
    if(self.player1.isExist_pawns(x,y) or self.player2.isExist_pawns(x,y)):
      return False
    else:
      return True
  
  def isKoordHome(self, player, x,y):
    if(player==1):
      return(self.player1.isExist_home(x,y))
    else:
      return(self.player2.isExist_home(x,y))
      
    
  def isKoordGoal(self, player, x,y):
    if(player==1):
      return(self.player1.isExist_goal(x,y))
    else:
      return(self.player2.isExist_goal(x,y))
  
  # def isValid(self, posX, posY, desX, desY):
  #   status = True
  #   if((desX >=1 and desX <= self.boardSize) and desY >=1 and desY <= self.boardSize):
  #     if((self.isEmpty(desX+1, desY)) or (self.isEmpty(desX,desY+1))):
  #       if((self.isEmpty(desX+2, desY)) and not(self.isEmpty(desX+1,desY)) or (self.isEmpty(desX, desY+2)) and not(self.isEmpty(desX,desY+1))):
          #departed
# c = Board(16, 10)
# print(c.isEmpty(6,4))