import pygame
from pygame.locals import *
import random
import time
from threading import Thread
from network import Network
from player import Player

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

fps = 9
update_snake = 0
food = [0, 0]
new_food = True
new_piece = [0, 0]
score = 0
score2 = 0
game_over = -1
clicked = False
game_duration = 140
time_left = game_duration
increment = 1  # how many segments you will grow when eat
cell_size = 20

bg = (179, 179, 179)
green = (31, 89, 47)
red = (120, 0, 0)
grid = (143, 143, 143)
food_col = (23, 23, 23)
black = (0, 0, 0)
white = (219, 219, 219)
almost_black = (15, 15, 15)
font = pygame.font.SysFont(None, 40)
again_rect = Rect(screen_width // 2 - 95, screen_height // 2, 190, 50)
clock = pygame.time.Clock()
ja = ""
n = Network()
if n.getP() == 0:
    p1 = Player(cell_size, screen_width/2 - 40, screen_height/2, green)
    p2 = Player(cell_size, screen_width/2 + 40, screen_height/2, red)
    ja = "left"
else:
    p2 = Player(cell_size, screen_width / 2 - 40, screen_height/2, green)
    p1 = Player(cell_size, screen_width / 2 + 40, screen_height/2, red)
    ja = "right"

run = True
timer_img = font.render('', True, black)


def draw_screen():
    screen.fill(bg)
    for x in range(int(screen_width / cell_size)):
        for y in range(int(screen_height / cell_size)):
            pygame.draw.rect(screen, grid, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, bg, (x * cell_size + 1, y * cell_size + 1, cell_size - 2, cell_size - 2))


def draw_score(x, y, x2, y2):
    # 1
    score_txt = 'Red score: ' + str(score)
    score_img = font.render(score_txt, True, black)
    screen.blit(score_img, (x, y))

    # 2
    score2_txt = 'Green score: ' + str(score2)
    score_img = font.render(score2_txt, True, black)
    screen.blit(score_img, (x2, y2))


def check_game_over(gmo, pla1, pla2):
    # if time left
    if gmo == 10:
        if score > score2:
            return 2
        elif score2 > score:
            return 1
        else:
            return 3

    # if snake eaten itself
    # 1
    head_count = 0
    snake_pos = pla1.snake_pos
    snake_pos2 = pla2.snake_pos
    for segment in snake_pos:
        if snake_pos[0] == segment and head_count > 0:
            gmo = 1
        head_count += 1
    for segment in snake_pos2:
        if snake_pos[0] == segment and head_count > 0:
            gmo = 1
        head_count += 1

    # 2
    head_count = 0
    for segment in snake_pos2:
        if snake_pos2[0] == segment and head_count > 0:
            gmo = 2
        head_count += 1
    head_count = 0
    for segment in snake_pos:
        if snake_pos2[0] == segment and head_count > 0:
            gmo = 2
        head_count += 1

    if snake_pos[0] == snake_pos2[0]:
        gmo = 3
    # if snake out of bounds
    # 1
    if pla1.is_out():
        gmo = 1
    # 2
    if pla2.is_out():
        gmo = 2

    return gmo


def draw_game_over(wynik):
    if (wynik == 2 and ja == "left") or (wynik == 1 and ja == "right"):
        over_txt = 'Green player win'
        over_img = font.render(over_txt, True, green)
        pygame.draw.rect(screen, almost_black, (screen_width // 2 - 120, screen_height // 2 - 60, 240, 50))
        screen.blit(over_img, (screen_width // 2 - 115, screen_height // 2 - 50))
        again_txt = "Play again?"
        again_img = font.render(again_txt, True, green)
    elif (wynik == 1 and ja == "left") or (wynik == 2 and ja == "right"):
        over_txt = 'Red player win'
        over_img = font.render(over_txt, True, red)
        pygame.draw.rect(screen, almost_black, (screen_width // 2 - 110, screen_height // 2 - 60, 220, 50))
        screen.blit(over_img, (screen_width // 2 - 100, screen_height // 2 - 50))
        again_txt = "Play again?"
        again_img = font.render(again_txt, True, red)
    else:
        over_txt = 'Draw'
        over_img = font.render(over_txt, True, white)
        pygame.draw.rect(screen, almost_black, (screen_width // 2 - 50, screen_height // 2 - 60, 100, 50))
        screen.blit(over_img, (screen_width // 2 - 35, screen_height // 2 - 50))
        again_txt = "Play again?"
        again_img = font.render(again_txt, True, white)

    pygame.draw.rect(screen, almost_black, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


def draw_waiting(t):
    text = 'Wait - ' + str(t)
    text_img = font.render(text, True, white)
    pygame.draw.rect(screen, almost_black, (screen_width // 2 - 90, screen_height // 2 - 60, 180, 50))
    screen.blit(text_img, (screen_width // 2 - 50, screen_height // 2 - 50))


def countdown():
    global timer_img
    global game_over
    global time_left
    global run
    while run:
        if game_over == -1:
            mins, secs = divmod(time_left, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            timer_img = font.render(timer, True, black)
            time.sleep(1)
            time_left -= 1
            if time_left <= 0:
                game_over = check_game_over(10, p1, p2)


t1 = Thread(target=countdown)
t1.start()
while run:
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            p1.turn(event)

    status = n.send("status")
    if status == -1:
        if game_over == -1:
            n.send("wait")
            update_snake = 0
            p1.step()
            p2.direction = n.send(p1.direction)
            p2.step()

        else:
            draw_game_over(game_over)
            if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked:
                clicked = False
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    update_snake = 0
                    food = [0, 0]
                    new_food = True
                    new_piece = [0, 0]
                    score = 0
                    score2 = 0
                    time_left = game_duration
                    if ja == "left":
                        p1.reset(screen_width / 2 - 40, screen_height/2)
                        p2.reset(screen_width / 2 + 40, screen_height/2)
                    else:
                        p2.reset(screen_width / 2 - 40, screen_height/2)
                        p1.reset(screen_width / 2 + 40, screen_height/2)
                    n.send("restart")
                    pygame.display.update()
            if n.send("both"):
                game_over = -1

        if new_food:
            if ja == "left":
                new_food = False
                food[0] = cell_size * random.randint(0, int(screen_width / cell_size) - 1)
                food[1] = cell_size * random.randint(0, int(screen_height / cell_size) - 1)
                n.send(food)
            else:
                food = n.send("get_food")

        game_over = check_game_over(game_over, p1, p2)
        pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

        # is food eaten?
        if p1.snake_pos[0] == food:
            score += 1
            new_food = True
            p1.new_piece(increment)

        if p2.snake_pos[0] == food:
            score2 += 1
            new_food = True
            p2.new_piece(increment)

        # drawing snake
        p1.draw(screen)
        p2.draw(screen)

        draw_score(5, 5, 5, 32)
        screen.blit(timer_img, (screen_width - 80, 8))
        update_snake += 1
        clock.tick(fps)
    else:
        game_over = -1
        update_snake = 0
        food = [0, 0]
        new_food = True
        new_piece = [0, 0]
        score = 0
        score2 = 0
        time_left = game_duration
        if ja == "left":
            p1.reset(screen_width / 2 - 40, screen_height / 2)
            p2.reset(screen_width / 2 + 40, screen_height / 2)
        else:
            p2.reset(screen_width / 2 - 40, screen_height / 2)
            p1.reset(screen_width / 2 + 40, screen_height / 2)
        n.send("restart")
        draw_waiting(status)
    pygame.display.update()

pygame.quit()
