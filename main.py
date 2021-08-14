import math

import pygame

from utils import *

BG_COLOR = (0, 0, 0)
PLAYER_POS_DIFF = 1

LIGHT_GREY = (220, 220, 220)
LIVES_MSG_POSITION = (10, 40)
COUNT_DOWN_MSG_POSITION = (10, 10)
START_MSG_POSITION = (10, 250)


def first_game_setup():
    pygame.init()
    game_status.level = 1
    game_status.running = True
    game_status.screen_size = (500, 500)
    game_status.screen = pygame.display.set_mode(game_status.screen_size)
    load_images_to_game_status()
    game_status.pause = {
        "is paused": True,
        "is beginning": True
    }
    game_status.restart = False


def init_level():
    pygame.display.set_caption("survival level: " + str(game_status.level))
    current_level_data = get_current_level_data(game_status.level)
    game_status.player = current_level_data["player"]
    game_status.enemies = current_level_data["enemies"]
    game_status.hearts = current_level_data["hearts"]
    game_status.count_down = {
        "total time": current_level_data["count down"] * 1000,
        "initial time": pygame.time.get_ticks(),
        "time left": current_level_data["count down"] * 1000
    }


def load_images_to_game_status():
    player_image = pygame.image.load('snail.png')
    player_image = pygame.transform.scale(player_image, (PLAYER_LENGTH, PLAYER_LENGTH))
    heart_image = pygame.image.load('good-mushroom.png')
    heart_image = pygame.transform.scale(heart_image, (HEART_LENGTH, HEART_LENGTH))
    enemy_image = pygame.image.load('sad-mushroom.png')
    enemy_image = pygame.transform.scale(enemy_image, (ENEMY_LENGTH, ENEMY_LENGTH))

    game_status.images = {
        "player": player_image,
        "heart": heart_image,
        "enemy": enemy_image
    }


def check_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_status.running = False


def draw_game():
    game_status.screen.fill(BG_COLOR)
    draw_player()
    draw_lives()
    draw_enemies()
    draw_hearts()
    draw_count_down_msg()
    pygame.display.update()


def draw_count_down_msg():
    font = pygame.font.Font(None, 50)
    count_down_msg = font.render("count down: " + str(math.ceil(game_status.count_down["time left"] / 1000)), True,
                                 LIGHT_GREY)
    game_status.screen.blit(count_down_msg, COUNT_DOWN_MSG_POSITION)


def draw_hearts():
    for heart in game_status.hearts:
        game_status.screen.blit(game_status.images["heart"], heart.position.to_tuple())


def draw_enemies():
    for enemy in game_status.enemies:
        game_status.screen.blit(game_status.images["enemy"], enemy.position.to_tuple())


def draw_lives():
    font = pygame.font.Font(None, 50)
    lives_msg = font.render("lives: " + str(game_status.player.lives), True, LIGHT_GREY)
    game_status.screen.blit(lives_msg, LIVES_MSG_POSITION)


def draw_player():
    player_pos = (game_status.player.position.x, game_status.player.position.y)
    game_status.screen.blit(game_status.images["player"], player_pos)


def update_player():
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP]:
        game_status.player.update_position(Position(0, -PLAYER_POS_DIFF))
    if pressed_keys[pygame.K_DOWN]:
        game_status.player.update_position(Position(0, PLAYER_POS_DIFF))
    if pressed_keys[pygame.K_LEFT]:
        game_status.player.update_position(Position(-PLAYER_POS_DIFF, 0))
    if pressed_keys[pygame.K_RIGHT]:
        game_status.player.update_position(Position(PLAYER_POS_DIFF, 0))

    game_status.player.restrict_in_screen(PLAYER_LENGTH, game_status.screen_size[0] - PLAYER_LENGTH, PLAYER_LENGTH,
                                          game_status.screen_size[1] - PLAYER_LENGTH)


def update_enemies():
    collided_enemies = [enemy for enemy in game_status.enemies if enemy.is_player_collision(game_status.player)]
    game_status.enemies = [enemy for enemy in game_status.enemies if not enemy.is_player_collision(game_status.player)]
    game_status.player.minus_lives(len(collided_enemies))


def update_heart():
    collided_heart = [heart for heart in game_status.hearts if heart.is_player_collision(game_status.player)]
    game_status.hearts = [heart for heart in game_status.hearts if not heart.is_player_collision(game_status.player)]
    for heart in collided_heart:
        game_status.player.add_lives(heart.lives)


def update():
    update_player()
    update_enemies()
    update_heart()
    update_count_down()
    update_game_by_lives()


def update_game_by_lives():
    if game_status.player.lives <= 0:
        game_status.restart = True


def update_count_down():
    curr_time = pygame.time.get_ticks()
    time_left = (game_status.count_down["initial time"] + game_status.count_down["total time"]) - curr_time
    game_status.count_down["time left"] = time_left
    if time_left < 0:
        game_status.pause["is paused"] = True
        game_status.pause["is beginning"] = False


def draw_level_start_msg():
    game_status.screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 30)
    start_msg = font.render("The game starts now. Level " + str(game_status.level), True, LIGHT_GREY)
    game_status.screen.blit(start_msg, START_MSG_POSITION)
    pygame.display.update()


def draw_level_end_msg():
    game_status.screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 30)
    start_msg = font.render("You survived. Next level start in 3 seconds", True, LIGHT_GREY)
    game_status.screen.blit(start_msg, START_MSG_POSITION)
    pygame.display.update()


def draw_game_restart_msg():
    game_status.screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 30)
    restart_msg = font.render("You are died. Should restart? y/n", True, LIGHT_GREY)
    game_status.screen.blit(restart_msg, START_MSG_POSITION)
    pygame.display.update()


def make_end_game_decision():
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_y]:
        game_status.restart = not game_status.restart
        # game_status.level = 1 # comment out if want to restart from last level
        init_level()
        game_status.pause["is paused"] = True
        game_status.pause["is beginning"] = True
    elif pressed_keys[pygame.K_n]:
        game_status.running = False


def check_winning():
    if get_max_level() < game_status.level + 1:
        draw_winning_msg()
        pygame.time.wait(3000)
        game_status.running = False


def draw_winning_msg():
    game_status.screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 30)
    restart_msg = font.render("You WIN", True, LIGHT_GREY)
    game_status.screen.blit(restart_msg, START_MSG_POSITION)
    pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_status = GameStatus()
    first_game_setup()
    while game_status.running:
        check_event()
        if game_status.pause["is paused"]:
            if game_status.pause["is beginning"]:
                draw_level_start_msg()
                pygame.time.wait(1000)
                game_status.pause["is paused"] = False
                init_level()
            else:
                draw_level_end_msg()
                pygame.time.wait(3000)
                check_winning()
                game_status.level += 1
                game_status.pause["is beginning"] = not game_status.pause["is beginning"]
        elif game_status.restart:
            draw_game_restart_msg()
            make_end_game_decision()
        else:
            update()
            draw_game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
