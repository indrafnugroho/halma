from player import Player
from coordinate import Coordinate
# from gui import BoardGUI
import math
import time
import copy

class Board:
  def __init__(self, boardSize, timeLimit, p1, p2, selfplay, bot):
    self.boardSize = boardSize
    self.timelimit = timeLimit
    self.player1 = p1
    self.player2 = p2
    self.g_player = p1 if p1.color == "GREEN" else p2
    self.r_player = p2 if p2.color == "RED" else p1
    self.turn = 1
    self.coordinate = [[Coordinate(i, j) for i in range(self.boardSize)] for j in range(self.boardSize)]
    self.depth = 3
    self.selfplay = selfplay
    self.bot = bot
    
    if self.boardSize == 8:
      maxIter = 4
    elif self.boardSize == 10:
      maxIter = 5
    else: # default is 16 x 16
      maxIter = 6

    for i in range(maxIter):
      for j in range(maxIter):
        if (i + j < maxIter and i < 6 and j < 6):
          self.coordinate[i][j].color = "RED"
          self.coordinate[i][j].pawn = 2
          self.r_player.homeCoord.append(self.coordinate[i][j])
          self.g_player.goalCoord.append(self.coordinate[i][j])
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].color = "GREEN"
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].pawn = 1
          self.g_player.goalCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])
          self.r_player.homeCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])

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
    return(player.isExist_home(x,y))
      
  def isKoordGoal(self, player, x, y):
    return(player.isExist_goal(x,y)) 
    
  def checkAvailablePosition(self, position, delta):
    # mengecek semua yang berdelta 1 itu kosong, dan gak melebihi size board
    # print("position checked = ", position)
    x, y = position
    availablePosition = []

    if (delta == 1):
      availablePosition.append((x+1, y))
      availablePosition.append((x+1, y+1))
      availablePosition.append((x, y+1))
      availablePosition.append((x-1, y+1))
      availablePosition.append((x-1, y))
      availablePosition.append((x-1, y-1))
      availablePosition.append((x, y-1))
      availablePosition.append((x+1, y-1))
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


    # if (delta == 1):
    #   print("available pos no jump = ", availablePosition)
    # else:
    #   print("available pos before jump = ", availablePosition)
    
    length = len(availablePosition)
    i = 0
    while (i < length):
      (x, y) = availablePosition[i]
      # jika diluar board
      if(x<1 or y<1 or x>self.boardSize or y>self.boardSize):
        # print(availablePosition[i], " is out of bond")
        availablePosition.remove(availablePosition[i])
        length -= 1

      # jika ada isinya
      elif (delta == 1 and not(self.isEmpty(x, y))):
        # print(availablePosition[i], " is filled")
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        # print(availablePosition[i], " is AVAILABLE!")
        i += 1
    return availablePosition

  def getJump(self, position, jumps, last_position):
    availableJumps = self.checkAvailablePosition(position, 2)
    # print("available jumps recursive = ", availableJumps)
    # print("last position = ", last_position)

    try:
      availableJumps.remove(last_position)
    except:
      pass

    if (len(availableJumps) ==  0):
      return jumps
    else:
      for i in range (len(availableJumps)):
        if availableJumps[i] not in jumps:
          jumps.append(availableJumps[i])
          self.getJump(availableJumps[i], jumps, position)
        
  def getAksiValid(self, pawn):
    if (self.player1.isExist_pawns(pawn.x, pawn.y)):
        player = self.player1
    else:
        player = self.player2

    # posisi saat ini
    current_position = (pawn.x, pawn.y)
    # print("current position = ", current_position)

    # available positions
    availablePosition = self.checkAvailablePosition(current_position, 1)
    # print("available positions = ", availablePosition)
    availableJump = self.checkAvailablePosition(current_position, 2)
    # print("available jumps = ", availableJump)

    if (len(availableJump) > 0):
      for i in range (len(availableJump)):
        if (availableJump[i] not in availablePosition):
          availablePosition.append(availableJump[i])
        # print("")
        # print ("current jump position = ", availableJump[i])
        jumps = []
        self.getJump(availableJump[i], jumps, current_position)
        if (len(jumps) > 0):
          for i in range (len(jumps)):
            # print("available positions 2 = ", availablePosition)
            # print("jumps                 = ", jumps[i])
            if (jumps[i] not in availablePosition):
              availablePosition.append(jumps[i])
        # print("s")
    
    # Cek keluar home atau masuk base
    length = len(availablePosition)
    i = 0
    while (i < length):
      (x, y) = availablePosition[i]
      if (pawn.IsArrived and not(self.isKoordGoal(player, x, y))) or (pawn.IsDeparted and (self.isKoordHome(player, x ,y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    availablePosition = sorted(availablePosition, key=lambda tup: (tup[0], tup[1]))
    # print("Available Position: ", availablePosition)
    return availablePosition

  def objectiveFunc(self, player):

    def point_distance(x1, y1, x2, y2):
      return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    val = 0

    ## Ini yang belom di ubah2

    for x in range(self.boardSize):
      for y in range(self.boardSize):
        c = self.coordinate[y][x]
        if (c.pawn == 1):
          goalDistance = point_distance(c.x, c.y, 0, 0)
          val -= goalDistance

        elif (c.pawn == 2):
          goalDistance = point_distance(c.x, c.y, self.boardSize-1, self.boardSize-1)
          val += goalDistance
        
    # print("val dari obj func", val)
    if player.color == "RED":
      val *= -1
    return val

  def minimax(self, depth, playermax, playermin, timelimit, isLocalSearch, a=float("-inf"), b=float("inf"), isMax=True):
    # basis
    if depth == 0 or time.time() > timelimit:
      return self.objectiveFunc(playermax), None

    bestmove = None
    if isMax:
      bestval = float("-inf")
      if isLocalSearch:
        possiblemoves = self.localSearch(playermax)
      else:
        possiblemoves = self.getPlayerMoves(playermax)
        
    else:
      bestval = float("inf")
      if isLocalSearch:
        possiblemoves = self.localSearch(playermin)
      else:
        possiblemoves = self.getPlayerMoves(playermin)

    # untuk setiap move yang mungkin
    for move in possiblemoves:
      for to in move["to"]:
        # keluar apabila melebihi timelimit
        if time.time() > timelimit:
          return bestval, bestmove

        # memindahkan sementara pion
        self.tempMovePawn((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))

        # minimax rekursif
        val, _ = self.minimax(depth - 1, playermax, playermin, timelimit, isLocalSearch, a, b, not isMax)

        # mengembalikan pion ke tempat semula
        self.tempMovePawn((to.y+1, to.x+1), (move["from"].y+1, move["from"].x+1))

        if isMax and val > bestval:
          bestval = val
          bestmove = ((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))
          a = max(a, val)

        if not isMax and val < bestval:
          bestval = val
          bestmove = ((move["from"].y+1, move["from"].x+1), (to.y+1, to.x+1))
          b = min(b, val)

        # alpha beta pruning
        if b <= a:
          return bestval, bestmove

    return bestval, bestmove

  # localsearch mengurangi jumlah move yang dapat diambil dari sebuah pion
  # dengan mengambil langkah tujuan yang memiliki value obj function paling besar
  def localSearch(self, player):
    possiblemoves = []
    for p in player.pawns:
      moves = []
      validactions = self.getAksiValid(p)
      if (len(validactions) == 0):
        continue
      else:
        temp = copy.deepcopy(p)
        (x, y) = validactions[0]
        validactions.remove((x, y))

        self.tempMovePawn((p.y, p.x), (y, x))
        bestval = self.objectiveFunc(player)
        self.tempMovePawn((y, x), (temp.y, temp.x))
        moves.append((x, y))
        
        for va in validactions:
          self.tempMovePawn((p.y, p.x), (va[1], va[0]))
          val = self.objectiveFunc(player)
          self.tempMovePawn((va[1], va[0]), (temp.y, temp.x))

          # player maximum
          if ((player.color == self.player1.color and self.turn == 1) or (player.color == self.player2.color and self.turn == 2)):
            if (val > bestval):
              moves.clear()
              moves.append((va[0], va[1]))
              bestval = val
            elif (val == bestval):
              moves.append((va[0], va[1]))
          #player minimum
          else:
            if (val < bestval):
              moves.clear()
              moves.append((va[0], va[1]))
              bestval = val
            elif (val == bestval):
              moves.append((va[0], va[1]))
        
        curr_tile = self.coordinate[p.y-1][p.x-1]
        move = {
          "from": curr_tile,
          "to": self.getMovesCoord(moves)
        }
        possiblemoves.append(move)
    
    return possiblemoves
          
  def getPlayerMoves(self, player):
    moves = []  # All possible moves
    for p in player.pawns:
      curr_tile = self.coordinate[p.y-1][p.x-1]
      move = {
        "from": curr_tile,
        "to": self.getMovesCoord(self.getAksiValid(p))
      }
      moves.append(move)
    return moves

  def getMovesCoord(self, validactions):
    moves = []
    for l in validactions:
      el = self.coordinate[l[1]-1][l[0]-1]
      moves.append(el)
    return moves

  def movePawn(self, from_coord, to_coord):
    from_tile = self.coordinate[from_coord[0]-1][from_coord[1]-1]
    to_tile = self.coordinate[to_coord[0]-1][to_coord[1]-1]
    
    # apabila pindah dari tile kosong atau pindah menuju tile yang ada pionnya
    if from_tile.pawn == 0 or to_tile.pawn != 0:
      print("Invalid move pawn!")
      return

    # memindahkan pion
    if from_tile.pawn == 1:
      self.g_player.movePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    elif from_tile.pawn == 2:
      self.r_player.movePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    else:
      print("Invalid move pawn!")
      return
    to_tile.pawn = from_tile.pawn
    from_tile.pawn = 0

  def tempMovePawn(self, from_coord, to_coord):
    from_tile = self.coordinate[from_coord[0]-1][from_coord[1]-1]
    to_tile = self.coordinate[to_coord[0]-1][to_coord[1]-1]
    
    # memindahkan sementara pion
    if from_tile.pawn == 1:
      self.g_player.tempMovePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    elif from_tile.pawn == 2:
      self.r_player.tempMovePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    else:
      print("invalid temp move pawn")
      return
    to_tile.pawn = from_tile.pawn
    from_tile.pawn = 0

  def executeBotMove(self):
    max_time = time.time() + self.timelimit

    # memanggil fungsi minimax search
    if (self.selfplay):
      playermax = self.player1 if self.turn == 1 else self.player2
      playermin = self.player2 if self.turn == 1 else self.player1
      if (self.turn == 2):
        _, move = self.minimax(self.depth, playermax, playermin, max_time, True)
      else:
        _, move = self.minimax(self.depth, playermax, playermin, max_time, False)
    else:
      playermax = self.player2
      playermin = self.player1
      if (self.bot == "MLS"):
        _, move = self.minimax(self.depth, playermax, playermin, max_time, True)
      else:
        _, move = self.minimax(self.depth, playermax, playermin, max_time, False)

    # memindahkan pion
    if move is None:
      print("Status: no action taken")
    else:
      (x1, y1) = move[0]
      (x2, y2) = move[1]
      self.movePawn((x1, y1), (x2, y2))
      print("Status: Pawn", (y1, x1), "moved to", (y2, x2))

  def getMoveFromTile(self, player, x, y):
    p = player.getPawn(x, y)
    return self.getAksiValid(p)