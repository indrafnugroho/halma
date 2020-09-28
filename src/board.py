from Player import Player

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
