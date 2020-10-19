from player import Player
from coordinate import Coordinate
# from gui import BoardGUI
import math
import time

class Board:
  def __init__(self, boardSize, timeLimit, player, bot):
    self.boardSize = boardSize
    self.player = player
    self.bot = bot
    self.g_player = player if player.color == "GREEN" else bot
    self.r_player = bot if bot.color == "RED" else player
    self.turn = "GREEN"
    self.coordinate = [[Coordinate(i, j) for i in range(self.boardSize)] for j in range(self.boardSize)]
    self.depth = 3
    # self.system = system
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
          self.coordinate[i][j].color = "RED"
          self.coordinate[i][j].pawn = 2
          self.g_player.homeCoord.append(self.coordinate[i][j])
          self.r_player.goalCoord.append(self.coordinate[i][j])
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].color = "GREEN"
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].pawn = 1
          self.r_player.goalCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])
          self.g_player.homeCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])

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
    if(self.player.isExist_pawns(x,y) or self.bot.isExist_pawns(x,y)):
      return False
    else:
      return True
  
  def isKoordHome(self, player, x, y):
    return(player.isExist_home(x,y))
      
  def isKoordGoal(self, player, x, y):
    return(player.isExist_goal(x,y)) 
    
  def checkAvailablePosition(self, position, delta):
    # mengecek semua yang berdelta 1 itu kosong, dan gak melebihi size board
    print("position checked = ", position)
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
    print("available jumps recursive = ", availableJumps)
    print("last position = ", last_position)

    try:
      availableJumps.remove(last_position)
    except:
      pass

    if (len(availableJumps) ==  0):
      return jumps
    else:
      for i in range (len(availableJumps)):
        jumps.append(availableJumps[i])
        self.getJump(availableJumps[i], jumps, position)
        
  def getAksiValid(self, pawn):
    if (self.player.isExist_pawns(pawn.x, pawn.y)):
        player = self.player
    else:
        player = self.bot

    # posisi saat ini
    current_position = (pawn.x, pawn.y)
    print("current position = ", current_position)

    # available positions
    availablePosition = self.checkAvailablePosition(current_position, 1)
    print("available positions = ", availablePosition)

    availableJump = self.checkAvailablePosition(current_position, 2)
    print("available jumps = ", availablePosition)

    if (len(availableJump) > 0):
      for i in range (len(availableJump)):
        availablePosition.append(availableJump[i])
        print ("current jump position = ", availableJump[i])
        jumps = []
        self.getJump(availableJump[i], jumps, current_position)
        if (len(jumps) > 0):
          for i in range (len(jumps)):
            if (jumps[i] not in availablePosition):
              availablePosition.append(jumps[i])
    
    # Cek keluar home atau masuk base
    length = len(availablePosition)
    i = 0
    while (i < length):
      (x, y) = availablePosition[i]
      if (pawn.IsArrived and (self.isKoordGoal(player, x, y))) or (pawn.IsDeparted and (self.isKoordHome(player, x ,y))):
        availablePosition.remove(availablePosition[i])
        length -= 1
      else:
        i += 1
    return availablePosition

  def objectiveFunc(self, player):

    def point_distance(x1, x2, y1, y2):
      return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    val = 0
    
    for c in self.coordinate:
      if (player.color == "GREEN" and c.pawn == 1):
        goalDistances = [point_distance(c.x, c.y, g.x, g.y) for g in player.goalCoord if g.pawn != 1]
        minGoalDistance = min(goalDistances)
        val += minGoalDistance

      elif (player.color == "RED" and c.pawn == 2):
        goalDistances = [point_distance(c.x, c.y, g.x, g.y) for g in player.goalCoord if g.pawn != 2]
        minGoalDistance = min(goalDistances)
        val += minGoalDistance
        
    return val*(-1)

  def minimax(self, depth, playermax, playermin, timelimit, a=float("-inf"), b=float("inf"), max=True):
    # Bottomed out base case
    if depth == 0 or time.time() > timelimit:
      return self.objectiveFunc(playermax), None

    # Setup initial variables and find moves
    bestmove = None
    if max:
      bestval = float("-inf")
      possiblemoves = self.getPlayerMoves(playermax)
    else:
      bestval = float("inf")
      possiblemoves = self.getPlayerMoves(playermin)

    # For each move
    for move in possiblemoves:
      for to in move["to"]:

        # Bail out when we're out of time
        if time.time() > timelimit:
          return bestval, bestmove

        # Move piece to the move outlined
        # piece = move["from"].piece
        # move["from"].piece = Tile.P_NONE
        # to.piece = piece

        # Recursively call self
        val, _ = self.minimax(depth - 1, playermax, playermin, timelimit, a, b, not max)

        # Move the piece back
        # to.piece = Tile.P_NONE
        # move["from"].piece = piece

        if max and val > bestval:
          bestval = val
          bestmove = (move["from"], to)
          a = max(a, val)

        if not max and val < bestval:
          bestval = val
          bestmove = (move["from"], to)
          b = min(b, val)

        if b <= a:
          return bestval, bestmove

    return bestval, bestmove

  def getPlayerMoves(self, player):
    moves = []  # All possible moves
    for p in player.pawns:
      curr_tile = (p.x, p.y)
      move = {
        "from": curr_tile,
        "to": self.getAksiValid(p)
      }
      moves.append(move)
    return moves

  def movePawn(self, from_coord, to_coord):
    from_tile = self.coordinate[from_coord[0]-1][from_coord[1]-1]
    to_tile = self.coordinate[to_coord[0]-1][to_coord[1]-1]
    # Handle trying to move a non-existant piece and moving into a piece
    if from_tile.pawn == 0 or to_tile.pawn != 0:
      print("Invalid move")
      return

    # Move piece
    if from_tile.pawn == 1:
      self.g_player.movePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    else:
      self.r_player.movePawn((from_tile.x+1, from_tile.y+1), (to_tile.x+1, to_tile.y+1))
    to_tile.pawn = from_tile.pawn
    from_tile.pawn = 0

  def executeBotMove(self):

    # Print out search information
    # current_turn = (self.total_plies // 2) + 1
    # print("Turn", current_turn, "Computation")
    # print("=================" + ("=" * len(str(current_turn))))
    # print("Executing search ...", end=" ")
    # sys.stdout.flush()

    # self.board_view.set_status("Computing next move...")
    # self.computing = True
    # self.board_view.update()
    max_time = time.time() + self.timelimit

    # Execute minimax search
    # start = time.time()
    _, move = self.minimax(self.depth, self.bot, self.player, max_time)
    # end = time.time()

    # Print search result stats
    # print("complete")
    # print("Time to compute:", round(end - start, 4))
    # print("Total boards generated:", boards)
    # print("Total prune events:", prunes)

    # Move the resulting piece
    # self.outline_tiles(None)  # Reset outlines
    move_from = self.coordinate[move[0][0]][move[0][1]]
    move_to = self.coordinate[move[1][0]][move[1][1]]
    self.movepawn(move_from, move_to)

    # self.board_view.draw_tiles(board=self.board)  # Refresh the board

    # winner = self.find_winner()
    # if winner:
    #     self.board_view.set_status("The " + ("green"
    #         if winner == Tile.P_GREEN else "red") + " player has won!")
    #     self.board_view.set_status_color("#212121")
    #     self.current_player = None
    #     self.current_player = None

    #     print()
    #     print("Final Stats")
    #     print("===========")
    #     print("Final winner:", "green"
    #         if winner == Tile.P_GREEN else "red")
    #     print("Total # of plies:", self.total_plies)

    # else:  # Toggle the current player
    #     self.current_player = (Tile.P_RED
    #         if self.current_player == Tile.P_GREEN else Tile.P_GREEN)

    # self.computing = False
    # print()

  def getMoveFromTile(self, player, x, y):
    p = player.getPawn(x, y)
    return self.getAksiValid(p)

# board = Board(8, 100, "GREEN", "CMD")



# if __name__ == "__main__":      
#   board = Board(8, 100, "GREEN", "CMD")
#   board.printBoard()
