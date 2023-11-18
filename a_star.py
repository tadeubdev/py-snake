from node import Node
from proximity_algorithm import Proximity_Algorithm
import pygame as pg

class A_Star(Proximity_Algorithm):
  def __init__(self, game, grid, maxTries = 1000) -> None:
    super().__init__(game, grid, maxTries)
    self.openSet = []
    self.closedSet = []
    self.path = []
    self.start = None
    self.end = None
    self.current = None
    self.grid = grid
    self.gridSizeX = len(grid)
    self.gridSizeY = len(grid[0])

  def addRecsToGrid(self, recs, value):
    for rec in recs:
      recX = rec.x // self.game.TILE_SIZE
      recY = rec.y // self.game.TILE_SIZE
      if recX < 0 or recX >= self.gridSizeX or recY < 0 or recY >= self.gridSizeY:
        continue
      self.grid[recX][recY] = value

  def generate(self, start, end):
    self.openSet = []
    self.closedSet = []
    self.start = Node(start.x // self.game.TILE_SIZE, start.y // self.game.TILE_SIZE)
    self.end = Node(end.x // self.game.TILE_SIZE, end.y // self.game.TILE_SIZE)
    self.openSet.append(self.start)
    self.current = self.openSet[0]
    for i in range(self.maxTries):
      self.current = self.getLowestFScore()
      if self.current and self.current.x == self.end.x and self.current.y == self.end.y:
        print(self.current)
        return self.retracePath()
      if self.openSet.count(self.current) > 0:
        self.openSet.remove(self.current)
      self.closedSet.append(self.current)
      neighbors = self.getNeighbors(self.current)
      for neighbor in neighbors:
        if neighbor in self.closedSet:
          continue
        tentativeGScore = self.current.gScore + self.getDistance(self.current, neighbor)
        if neighbor not in self.openSet:
          self.openSet.append(neighbor)
        elif tentativeGScore >= neighbor.gScore:
          continue
        neighbor.parent = self.current
        neighbor.gScore = tentativeGScore
        neighbor.fScore = neighbor.gScore + self.getDistance(neighbor, self.end)
    return False
  
  def getLowestFScore(self):
    if len(self.openSet) == 0:
      return None
    lowest = self.openSet[0]
    for node in self.openSet:
      if node.fScore < lowest.fScore:
        lowest = node
    return lowest
  
  def getDistance(self, nodeA, nodeB):
    return abs(nodeA.x - nodeB.x) + abs(nodeA.y - nodeB.y)
  
  def getNeighbors(self, node):
    if node == None or node.x < 0 or node.x >= self.gridSizeX or node.y < 0 or node.y >= self.gridSizeY:
      return []
    neighbors = []
    if node.x > 0 and self.grid[node.x - 1][node.y] == 0:
      neighbors.append(Node(node.x - 1, node.y))
    if node.x < self.gridSizeX - 1 and self.grid[node.x + 1][node.y] == 0:
      neighbors.append(Node(node.x + 1, node.y))
    if node.y > 0 and self.grid[node.x][node.y - 1] == 0:
      neighbors.append(Node(node.x, node.y - 1))
    if node.y < self.gridSizeY - 1 and self.grid[node.x][node.y + 1] == 0:
      neighbors.append(Node(node.x, node.y + 1))
    return neighbors
  
  def retracePath(self):
    self.path = []
    node = self.current
    while node.parent != None:
      self.path.append((node.x, node.y))
      if node.parent == self.start:
        break
      node = node.parent
    self.path.reverse()
    return self.path
  
  def draw(self):
    for node in self.openSet:
      node.draw('blue')
    for node in self.closedSet:
      node.draw('red')
    for node in self.path:
      node.draw('green')
    self.start.draw('yellow')
    self.end.draw('yellow')
    self.current.draw('orange')
    super().draw()
