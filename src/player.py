import copy

class Player:
  def __init__(self, color, boardSize):
    self.color = color
    self.makeRegionPawns(boardSize)
    self.homeCoord = []
    self.goalCoord = []
    
  def makeRegionPawns(self, boardSize):
    self.pawns = []
    self.home = []
    self.goal = []
    if boardSize == 8:
      maxIter = 5
    elif boardSize == 10:
      maxIter = 6
    else: # default is 16 x 16
      maxIter = 7

    for i in range(1, maxIter):
      for j in range(1, maxIter):
        if (i + j <= maxIter and i < maxIter and j < maxIter):
          self.pawns.append(Pion(boardSize - j + 1, boardSize - i + 1))
          self.home.append((boardSize - j + 1, boardSize - i + 1))
          self.goal.append((j, i))

    if self.color == 'RED':
      # If an opposing player
      temp = copy.deepcopy(self.home)
      self.home = copy.deepcopy(self.goal)
      self.goal = temp
      for i in range(len(self.pawns)):
        self.pawns[i].x = self.home[i][0]
        self.pawns[i].y = self.home[i][1]
              

  def printStatus(self):
    print('Color: '+ self.color)
    print('Position of pawns:')
    for pawn in self.pawns:
      print('({x}, {y}), IsArrived={IsArrived}, IsDeparted={IsDeparted}'.format(x=pawn.x, y=pawn.y, IsArrived=pawn.IsArrived, IsDeparted=pawn.IsDeparted))
  
  #all pawn in oponent base
  def isTerminate(self):
    status = True
    for p in self.pawns:
        if (p.x, p.y) in self.goal:
            status = True
        else:
            status = False
            break
    return status
  
  #cek if pawns contain x and y, true if yes
  def isExist_pawns(self,x,y):
    for i in range(len(self.pawns)):
      if(self.pawns[i].x == x and self.pawns[i].y== y ):
        return True
        break
      else:
        pass
    return False
  
  def isExist_home(self,x,y):
    koor =(x, y)
    if koor in self.home:
      return True
    else:
      return False
    
  def isExist_goal(self,x,y):
    koor =(x, y)
    if koor in self.goal:
      return True
    else:
      return False
  
  def getPawn(self, row, column):
    i = 0
    found = False
    while i < len(self.pawns) and not(found):
      if (self.pawns[i].x == row and self.pawns[i].y == column):
        pawn = self.pawns[i]
        return pawn
        found = True
      else:
        i +=1

  def tempMovePawn(self, from_tile, to_tile):
    (x, y) = from_tile
    (x2, y2) = to_tile
    for p in self.pawns:
      if p.x == x and p.y == y:
        p.x = x2
        p.y = y2
        self.pawns = sorted(self.pawns, key=lambda p: (p.x, p.y))
        break

  def movePawn(self, from_tile, to_tile):
    (x, y) = from_tile
    (x2, y2) = to_tile
    for p in self.pawns:
      if p.x == x and p.y == y:
        if (x, y) in self.home and (x2, y2) not in self.home:
          p.IsDeparted = True
        elif (x, y) not in self.goal and (x2, y2) in self.goal:
          p.IsArrived = True
        p.x = x2
        p.y = y2
        self.pawns = sorted(self.pawns, key=lambda p: (p.x, p.y))
        break

class Pion:
  def __init__(self, x, y):
    self.setCoordinate(x, y)
    self.setIsDeparted(False)
    self.setIsArrived(False)

  def setCoordinate(self,x, y):
    self.x = x
    self.y = y

  def setIsDeparted(self, IsDeparted):
    self.IsDeparted = IsDeparted
    
  def setIsArrived(self, IsArrived):
    self.IsArrived = IsArrived
  
  def getCoordinateX(self):
    return (self.x)
  
  def getCoordinateY(self):
    return (self.y)
  
  def getCoordinate(self):
    return (self.x, self.y)