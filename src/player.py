
class Player:
  def __init__(self, color, boardSize):
    self.color = color
    self.makeRegionPawns(boardSize)
    self.home = []
    self.goal = []
    
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
          print ("i = " + str(i) + " j = " + str(j))
          self.pawns.append(Pion(i, j))
          self.home.append((i, j))
          self.goal.append((boardSize - i + 1, boardSize - j + 1))

    if self.color == 'RED':
      # If an opposing player
      temp = self.home.copy()
      self.home = self.goal.copy()
      self.goal = temp
      for i in range(0, len(self.home)):
        self.pawns[i].x = self.home[i][0]
        self.pawns[i].y = self.home[i][1]
              

  def printStatus(self):
    print('Color: '+ self.color)
    print('Position of pawns:')
    for pawn in self.pawns:
      print('({x}, {y})'.format(x=pawn.x, y=pawn.y))
  
  #all pawn in oponent base
  def isTerminate(self):
    goal = self.goal
    pawns = self.pawns
    status = True
    for i in range(len(pawns)):
        pion = (pawns[i].x, pawns[i].y)
        if pion in goal:
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
    while (i < len(self.pawns)):
      print (self.pawns[i].x, self.pawns[i].y)
      if (self.pawns[i].x == row and self.pawns[i].y == column):
        pawn = self.pawns[i]
        return pawn
        found = True
      else:
        i +=1


        

# 8, 10, 16
# 10, 15, 19


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

# a = Player('BLACK', 10)
# a.printStatus()
# a = Player('WHITE', 10)
# a.printStatus()
# print(a.home)
# print(a.isExist_home(8,9))
# print(a.isTerminate())