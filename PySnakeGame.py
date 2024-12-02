import pygame as pg
from random import randrange
import sys
pg.init()

WINDOW = 720
TILE_SIZE = 25
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 120
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)
pg.display.set_caption("PySnake Game")
score = 0
high_score = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            sys.exit()
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and dirs[pg.K_w] or event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_s and dirs[pg.K_s] or event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1, pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_a and dirs[pg.K_a] or event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if event.key == pg.K_d and dirs[pg.K_d] or event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1, pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}
    screen.fill('grey15')
    # Draw Score
    font = pg.font.Font('Daydream.ttf', 18)
    text = font.render(f'Score: {score}     Best: {high_score}', True, 'white')
    screen.blit(text, (10,10))
    # Check Borders and Selfeating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        score, length, snake_dir = 0, 1, (0, 0)
        segments = [snake.copy()]
    # Check Food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        score += 1
        if score > high_score:
            high_score += 1
    # Draw Food
    pg.draw.rect(screen, 'gold2', food)
    # Draw Snake
    [pg.draw.rect(screen, 'dodgerblue3', segment) for segment in segments]
    # Move Snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip()
    clock.tick(60)