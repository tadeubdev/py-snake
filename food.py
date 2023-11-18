import pygame as pg
from random import randrange

vec2 = pg.math.Vector2

class Food:
  def __init__(self, game) -> None:
    self.game = game
    self.size = game.TILE_SIZE
    self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
    self.rect.center = self.get_random_position()

  def draw(self):
    pg.draw.rect(self.game.screen, 'red', self.rect)

  def reset(self):
    self.rect.center = self.get_random_position()

  def get_random_position(self):
    return [randrange(self.size // 2, self.game.SCREEN_SIZE[0] - self.size // 2, self.size),
            randrange(self.size // 2, self.game.SCREEN_SIZE[1] - self.size // 2, self.size)]
