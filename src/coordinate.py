# coordinate.py

class Coordinate:
    def __init__(self, x, y, color="BLACK", pawn=0):
        self.x = x
        self.y = y
        self.color = color
        self.pawn = pawn
        
    def setColor(self, color):
        self.color = color

    def setPawn(self, pawn):
        self.pawn = pawn

    def printCoordinate(self):
        print(str(self.x) + str(self.y) + self.color + str(self.pawn))