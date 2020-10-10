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
  
  def isKoordHome(self, player, x, y):
    if(player==1):
      return(self.player1.isExist_home(x,y))
    else:
      return(self.player2.isExist_home(x,y))
      
    
  def isKoordGoal(self, player, x, y):
    if(player==1):
      return(self.player1.isExist_goal(x,y))
    else:
      return(self.player2.isExist_goal(x,y)) 
    
  def checkAvailablePosition(self, position):
    # mengecek semua yang berdelta 1 itu kosong, dan gak melebihi size board
    x, y = position
    availablePosition = []

    availablePosition += (x+1,y)
    availablePosition += (x-1,y)
    availablePosition += (x,y+1)
    availablePosition += (x,y-1)
    availablePosition += (x+1,y+1)
    availablePosition += (x+1,y-1)
    availablePosition += (x-1,y-1)
    availablePosition += (x-1,y+1)

    length = len(availablePosition)
    i = 0

    while (i < length):
      x, y = availablePosition[i]
      # jika diluar board
      if(x< 1 or y<1 or x>self.boardSize or y>self.boardSize):
        availablePosition.remove(availablePosition[i])
        length -= 1

      # jika ada isinya
      elif not(self.isEmpty()):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    
    return availablePosition
        
        
  def getAksiValid(self, pawn):
    if (self.player1.isExist_Pawns(pawn.getCoordinateX, pawn.getCoordinateY)):
        player = self.player1
    else:
        player = self.player2

    aksi = []
    current_position = pawn.getCoordinate()
    availablePosition = self.checkAvailablePosition(current_position)
    # Cek keluar home atau masuk base
    length = len(availablePosition)
    i = 0
    while (i < length):
      x, y = availablePosition[i]
      if (pawn.isArrived and (self.isKoordGoal(player, x, y))) or (pawn.isDeparted and (self.isKoordHome(player, x ,y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1

    
    
  # def isValid(self, posX, posY, desX, desY):
  #   status = True
  #   if((desX >=1 and desX <= self.boardSize) and desY >=1 and desY <= self.boardSize):
  #     if((self.isEmpty(desX+1, desY)) or (self.isEmpty(desX,desY+1))):
  #       if((self.isEmpty(desX+2, desY)) and not(self.isEmpty(desX+1,desY)) or (self.isEmpty(desX, desY+2)) and not(self.isEmpty(desX,desY+1))):
          #departed

if __name__ == "__main__":      
  c = Board(16, 10)
  print(c.isEmpty(6,4))
