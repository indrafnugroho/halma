from player import Player
from coordinate import Coordinate
# from gui import BoardGUI
import math

class Board:
  def __init__(self, boardSize, timeLimit, player, system):
    if (player == "GREEN"):
      bot = "RED"
    elif (player == "RED"):
      bot = "GREEN"
    else:
      player = "GREEN"
      bot = "RED"
      self.selfplay = True
    
    self.boardSize = boardSize
    self.player1 = Player(player, boardSize)
    self.player2 = Player(bot, boardSize)
    self.turn = self.player1
    self.coordinate = [[Coordinate(i, j) for i in range(self.boardSize)] for j in range(self.boardSize)]
    # for i in range(8):
    #   for j in range(8):
    #     self.coordinate[i][j].printCoordinate()
    self.depth = 3
    self.system = system
    # if (system == "GUI"):
    #   self.GUI = BoardGUI(self.oa)
    
    if self.boardSize == 8:
      maxIter = 4
    elif self.boardSize == 10:
      maxIter = 5
    else: # default is 16 x 16
      maxIter = 6

    for i in range(maxIter):
      for j in range(maxIter):
        if (i + j < maxIter and i < 6 and j < 6):
          self.coordinate[i][j].color = player
          self.coordinate[i][j].pawn = 1 if player == "GREEN" else 2
          self.player1.home.append(self.coordinate[i][j])
          self.player2.goal.append(self.coordinate[i][j])
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].color = bot
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].pawn = 2 if bot == "RED" else 1
          self.player1.goal.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])
          self.player2.home.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])

  def printBoard(self):
    for i in range(self.boardSize + 1):
      if (i == 0):
        print("    ", end="")
        for j in range(self.boardSize):
          if j < self.boardSize - 1:
            print(chr(j+97) + " ", end="")
          else:
            print(chr(j+97) + " ")
      else:
        num = str(i) + "   " if i < 10 else str(i) + "  "
        print(num, end="")
        for j in range(self.boardSize):
          if j < self.boardSize - 1:
            if (self.coordinate[i-1][j].pawn == 1):
              print("G ", end="")
            elif (self.coordinate[i-1][j].pawn == 2):
              print("R ", end="")
            else:
              print("* ", end="")
          else:
            if (self.coordinate[i-1][j].pawn == 1):
              print("G ")
            elif (self.coordinate[i-1][j].pawn == 2):
              print("R ")
            else:
              print("* ")
  
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
    x, y = position
    availablePosition = []

    availablePosition += (x+delta, y)
    availablePosition += (x-delta, y)
    availablePosition += (x, y+delta)
    availablePosition += (x, y-delta)
    availablePosition += (x+delta, y+delta)
    availablePosition += (x+delta, y-delta)
    availablePosition += (x-delta, y-delta)
    availablePosition += (x-delta, y+delta)

    length = len(availablePosition)
    i = 0

    while (i < length):
      x, y = availablePosition[i]
      # jika diluar board
      if(x<1 or y<1 or x>self.boardSize or y>self.boardSize):
        availablePosition.remove(availablePosition[i])
        length -= 1

      # jika ada isinya
      elif not(self.isEmpty()):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    
    return availablePosition

  def getJump(self, position, jumps, last_position):
    availableJumps = self.checkAvailablePosition(position, 2) 
    availableJumps.remove(last_position)
    if (len(availableJumps) ==  0):
      return jumps
    else:
      for i in range (len(availableJumps)):
        jumps += availableJumps[i]
        self.getJump(availableJumps[i], jumps, position)
        
  def getAksiValid(self, pawn):
    if (self.player1.isExist_Pawns(pawn.getCoordinateX, pawn.getCoordinateY)):
        player = self.player1
    else:
        player = self.player2

    current_position = pawn.getCoordinate()
    availablePosition = self.checkAvailablePosition(current_position, 1)
    availableJump = self.checkAvailablePosition(current_position,2)
    for i in range (len(availableJump)):
      jumps = []
      getJump(availableJump[i], jumps, current_position)
      availableJump += jumps
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

  def objectiveFunc(self, player):

    def point_distance(x1, x2, y1, y2):
      return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    val = 0

    for c in self.coordinate:
      if (player.color == "GREEN" and c.pawn == 1):
        goalDistances = [point_distance(c.x, c.y, g.x, g.y) for g in player.goal if g.pawn != 1]
        minGoalDistance = min(goalDistances)
        val += minGoalDistance

      elif (player.color == "RED" and c.pawn == 2):
        goalDistances = [point_distance(c.x, c.y, g.x, g.y) for g in player.goal if g.pawn != 2]
        minGoalDistance = min(goalDistances)
        val += minGoalDistance
        
    return val

  def minimax(self, depth, playermax, timelimit, a=float("-inf"), b=float("inf"), max=True):
    # Bottomed out base case
    if depth == 0 or self.find_winner():
      return self.objectiveFunc(playermax), None

    # Setup initial variables and find moves
    bestmove = None
    if max:
      bestval = float("-inf")
      # possiblemoves = self.get_next_moves(playermax.color)
    else:
      bestval = float("inf")
      # possiblemoves = self.get_next_moves(("RED" if playermax.color == "GREEN" else "GREEN"))

    # For each move
    for move in possiblemoves:
      for to in move["to"]:

        # Bail out when we're out of time
        if time.time() > max_time:
          return best_val, best_move, prunes, boards

        # Move piece to the move outlined
        # piece = move["from"].piece
        # move["from"].piece = Tile.P_NONE
        # to.piece = piece

        # Recursively call self
        val, _, = self.minimax(self.depth - 1, playermax, timelimit, a, b, not max)

        # Move the piece back
        # to.piece = Tile.P_NONE
        # move["from"].piece = piece

        if max and val > bestval:
          bestval = val
          bestmove = (move["from"].loc, to.loc)
          a = max(a, val)

        if not max and val < bestval:
          bestval = val
          bestmove = (move["from"].loc, to.loc)
          b = min(b, val)

        if b <= a:
          return bestval, bestmove

    return bestval, bestmove
    
  # def isValid(self, posX, posY, desX, desY):
  #   status = True
  #   if((desX >=1 and desX <= self.boardSize) and desY >=1 and desY <= self.boardSize):
  #     if((self.isEmpty(desX+1, desY)) or (self.isEmpty(desX,desY+1))):
  #       if((self.isEmpty(desX+2, desY)) and not(self.isEmpty(desX+1,desY)) or (self.isEmpty(desX, desY+2)) and not(self.isEmpty(desX,desY+1))):
          #departed

if __name__ == "__main__":      
  board = Board(8, 100, "GREEN", "CMD")
  board.printBoard()