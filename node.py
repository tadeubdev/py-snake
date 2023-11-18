class Node:
  def __init__(self, x=0, y=0, gScore=0, fScore=0, parent=None):
    self.x = x
    self.y = y
    self.gScore = gScore
    self.fScore = fScore
    self.parent = parent

  def debug(self):
    print(f'Node: x={self.x}, y={self.y}, gScore={self.gScore}, fScore={self.fScore}, parent={self.parent}')
