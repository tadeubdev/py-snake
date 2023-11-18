import pygame as pg
from snake import Snake
from food import Food
from a_star import A_Star

class Game:
  def __init__(self) -> None:
    pg.init()
    self.SCREEN_SIZE = (800, 600)
    self.TILE_SIZE = 50
    self.screen = pg.display.set_mode(self.SCREEN_SIZE)
    self.clock = pg.time.Clock()
    self.grid = [[0 for _ in range(self.SCREEN_SIZE[1] // self.TILE_SIZE)] for _ in range(self.SCREEN_SIZE[0] // self.TILE_SIZE)]
    self.algorithm = A_Star(self, self.grid)
    self.new_game()

  def draw_grid(self):
    # draw a grid with transparency
    for x in range(0, self.SCREEN_SIZE[0], self.TILE_SIZE):
      pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.SCREEN_SIZE[1]))
    for y in range(0, self.SCREEN_SIZE[1], self.TILE_SIZE):
      pg.draw.line(self.screen, [50] * 3, (0, y), (self.SCREEN_SIZE[0], y))
    # draw the border
    pg.draw.rect(self.screen, [50] * 3, (0, 0, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1]), 1)

  def new_game(self):
    self.snake = Snake(self)
    self.food = Food(self)

  def update(self):
    self.snake.update()
    self.check_food_eaten()
    pg.display.flip()
    self.clock.tick(200)

  def runAlgorithm(self):
    self.algorithm.addRecsToGrid(self.snake.segments, 2)
    best_path = self.algorithm.generate(self.snake.rect, self.food.rect)
    if best_path:
      self.snake.new_point(best_path)
    else:
      self.new_game()

  def draw(self):
    self.screen.fill('black')
    self.draw_grid()
    self.snake.draw()
    self.food.draw()
    # self.runAlgorithm()
  
  def check_food_eaten(self):
    if self.snake.rect.colliderect(self.food.rect):
      self.snake.grow()
      self.food.reset()

  def check_event(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()
      # dispatch event to snake
      self.snake.control(event)

  def run(self):
    while True:
      self.check_event()
      self.update()
      self.draw()

if __name__ == "__main__":
  game = Game()
  game.run()