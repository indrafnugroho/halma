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
    
  def checkAvailablePosition(self, position, delta):
    # mengecek semua yang berdelta 1 itu kosong, dan gak melebihi size board
    print("position checked = ", position)
    x, y = position
    availablePosition = []

    if (delta == 1):
      availablePosition.append((x+1, y))
      availablePosition.append((x-1, y))
      availablePosition.append((x, y+1))
      availablePosition.append((x, y-1))
      availablePosition.append((x+1, y+1))
      availablePosition.append((x+1, y-1))
      availablePosition.append((x-1, y-1))
      availablePosition.append((x-1, y+1))
    else:
      if (not(self.isEmpty(x+1,y)) and (self.isEmpty(x+2, y))):
        availablePosition.append((x+2, y))
      if (not(self.isEmpty(x-1,y)) and (self.isEmpty(x-2, y))):
        availablePosition.append((x-2, y))
      if (not(self.isEmpty(x,y+1)) and (self.isEmpty(x, y+2))):
        availablePosition.append((x, y+2))
      if (not(self.isEmpty(x,y-1)) and (self.isEmpty(x, y-2))):
        availablePosition.append((x, y-2))
      if (not(self.isEmpty(x+1,y+1)) and (self.isEmpty(x+2, y+2))):
        availablePosition.append((x+2, y+2))
      if (not(self.isEmpty(x+1,y-1)) and (self.isEmpty(x+2, y-2))):
        availablePosition.append((x+2, y-2))
      if (not(self.isEmpty(x-1,y+1)) and (self.isEmpty(x-2, y+2))):
        availablePosition.append((x-2, y+2))
      if (not(self.isEmpty(x-1,y-1)) and (self.isEmpty(x-2, y-2))):
        availablePosition.append((x-2, y-2))


    if (delta == 1):
      print("available pos no jump = ", availablePosition)
    else:
      print("available pos before jump = ", availablePosition)
    length = len(availablePosition)
    i = 0

    while (i < length):
      (x, y) = availablePosition[i]
      print(availablePosition[i])
      # jika diluar board
      if(x<1 or y<1 or x>self.boardSize or y>self.boardSize):
        print("out of bond")
        availablePosition.remove(availablePosition[i])
        length -= 1

      # jika ada isinya
      elif (delta == 1 and not(self.isEmpty(x, y))):
        print("filled")
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    return availablePosition

  def getJump(self, position, jumps, last_position):
    availableJumps = self.checkAvailablePosition(position, 2)
    print("available jumps = ", availableJumps)
    print("last position = ", last_position)

    try:
      availableJumps.remove(last_position)
    except:
      pass

    if (len(availableJumps) ==  0):
      return jumps
    else:
      for i in range (len(availableJumps)):
        jumps += availableJumps[i]
        self.getJump(availableJumps[i], jumps, position)
        
  def getAksiValid(self, pawn):
    if (self.player1.isExist_pawns(pawn.x, pawn.y)):
        player = self.player1
    else:
        player = self.player2

    # posisi saat ini
    current_position = (pawn.x, pawn.y)
    print("current position = ", current_position)

    # available positions
    availablePosition = self.checkAvailablePosition(current_position, 1)
    print("available positions = ", availablePosition)

    availableJump = self.checkAvailablePosition(current_position, 2)
    print("available jumps = ", availablePosition)

    print("available position before start recursive = ", availablePosition)
    if (len(availableJump) > 0):
      for i in range (len(availableJump)):
        availablePosition.append(availableJump[i])
        ("current jump position = ", availableJump[i])
        jumps = []
        self.getJump(availableJump[i], jumps, current_position)
        if (len(jumps) > 0):
          for i in range (len(jumps)):
            availablePosition.append(jumps[i])
    
    # Cek keluar home atau masuk base
    length = len(availablePosition)
    i = 0
    while (i < length):
      if (pawn.IsArrived and (self.IsKoordGoal(player, x, y))) or (pawn.IsDeparted and (self.IsKoordHome(player, x ,y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    return availablePosition

    
    
  # def isValid(self, posX, posY, desX, desY):
  #   status = True
  #   if((desX >=1 and desX <= self.boardSize) and desY >=1 and desY <= self.boardSize):
  #     if((self.isEmpty(desX+1, desY)) or (self.isEmpty(desX,desY+1))):
  #       if((self.isEmpty(desX+2, desY)) and not(self.isEmpty(desX+1,desY)) or (self.isEmpty(desX, desY+2)) and not(self.isEmpty(desX,desY+1))):
          #departed

