import pygame as pg

vec2 = pg.math.Vector2

class Snake:
  def __init__(self, game) -> None:
    self.game = game
    self.size = game.TILE_SIZE
    self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
    self.direction = vec2(0, 0)
    self.step_delay = 150
    self.time = 0
    self.length = 1
    self.segments = []
    self.segments_best_path = []
    for i in range(self.length):
      rec = self.rect.copy()
      rec.x += i * self.size
      self.segments.append(rec)
    self.rect = self.segments[-1]
    self.dictionary = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

  def control(self, event):
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_UP and self.dictionary[pg.K_UP]:
        self.direction = vec2(0, -self.size)
        self.dictionary[pg.K_UP] = 1
        self.dictionary[pg.K_DOWN] = 0
        self.dictionary[pg.K_LEFT] = 1
        self.dictionary[pg.K_RIGHT] = 1
      elif event.key == pg.K_DOWN and self.dictionary[pg.K_DOWN]:
        self.direction = vec2(0, self.size)
        self.dictionary[pg.K_UP] = 0
        self.dictionary[pg.K_DOWN] = 1
        self.dictionary[pg.K_LEFT] = 1
        self.dictionary[pg.K_RIGHT] = 1
      elif event.key == pg.K_LEFT and self.dictionary[pg.K_LEFT]:
        self.direction = vec2(-self.size, 0)
        self.dictionary[pg.K_UP] = 1
        self.dictionary[pg.K_DOWN] = 1
        self.dictionary[pg.K_LEFT] = 1
        self.dictionary[pg.K_RIGHT] = 0
      elif event.key == pg.K_RIGHT and self.dictionary[pg.K_RIGHT]:
        self.direction = vec2(self.size, 0)
        self.dictionary[pg.K_UP] = 1
        self.dictionary[pg.K_DOWN] = 1
        self.dictionary[pg.K_LEFT] = 0
        self.dictionary[pg.K_RIGHT] = 1

  def delta_time(self):
    time_now = pg.time.get_ticks()
    if time_now - self.time > self.step_delay:
      self.time = time_now
      return True
    return False
  
  def grow(self):
    self.length += 1

  def check_borders(self):
    if self.rect.left < 0 or self.rect.right > self.game.SCREEN_SIZE[0]:
      self.game.new_game()
    if self.rect.top < 0 or self.rect.bottom > self.game.SCREEN_SIZE[1]:
      self.game.new_game()

  def check_self_collision(self):
    for segment in self.segments[:-1]:
      if self.rect.colliderect(segment):
        self.game.new_game()

  def move(self):
    if self.delta_time():
      if self.segments_best_path:
        best_segment = self.segments_best_path.pop(0)
        direction = ''
        if best_segment.x < self.rect.x:
          direction = 'left'
        elif best_segment.x > self.rect.x:
          direction = 'right'
        elif best_segment.y < self.rect.y:
          direction = 'up'
        elif best_segment.y > self.rect.y:
          direction = 'down'
        #
        if direction != '':
          self.control(pg.event.Event(pg.KEYDOWN, {'key': eval(f'pg.K_{direction.upper()}')}))
      self.rect.move_ip(self.direction)
      self.segments.append(self.rect.copy())
      self.segments = self.segments[-self.length:]
  
  def new_point(self, points):
    self.segments_best_path = [vec2(point[0] * self.size, point[1] * self.size) for point in points]

  def update(self):
    self.check_borders()
    self.move()

  def draw(self):
    for segment in self.segments:
      pg.draw.rect(self.game.screen, 'green', segment)
