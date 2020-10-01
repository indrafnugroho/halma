class Player:
  def __init__(self, color, boardSize):
    self.color = color
    self.makeRegionPawns(boardSize)

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
        if (i + j <= maxIter and i < 6 and j < 6):
          self.pawns.append(Pion(i, j))
          self.home.append((i, j))
          self.goal.append((boardSize - i + 1, boardSize - j + 1))

    if self.color == 'BLACK':
      # If an opposing player
      temp = self.home.copy()
      self.home = self.goal.copy()
      self.goal = temp

  def printStatus(self):
    print('Color: '+ self.color)
    print('Position of pawns:')
    for pawn in self.pawns:
      print('({x}, {y})'.format(x=pawn.x, y=pawn.y))

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

# a = Player('BLACK', 10)
# a.printStatus()