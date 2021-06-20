import pygame

from utils import *

game_status = GameStatus()

PLAYER_COLOR = (0, 0, 225)
ENEMY_COLOR = (225, 0, 0)
HEART_COLOR = (0, 225, 0)
BG_COLOR = (0, 0, 0)

PLAYER_RADIUS = 30
ENEMY_RADIUS = 50
HEART_RADIUS = 20

PLAYER_POS_DIFF = 5


def game_setup():
    pygame.init()
    pygame.display.set_caption("survival")


def init_game_status():
    game_status.enemies = [Enemy(position=Position(
        100, 100), lives=1, radius=ENEMY_RADIUS)]
    game_status.hearts = [Heart(Position(400, 400), HEART_RADIUS, 1)]
    game_status.running = True
    game_status.screen_size = (500, 500)
    game_status.screen = pygame.display.set_mode(game_status.screen_size)
    game_status.player_start_position = Position(250, 400)
    game_status.player = Player(
        position=game_status.player_start_position, lives=3, radius=PLAYER_RADIUS)


def first_game_setup():
    init_game_status()
    game_setup()


def draw_player():
    player_pos = (game_status.player.position.x, game_status.player.position.y)
    pygame.draw.circle(game_status.screen, PLAYER_COLOR,
                       player_pos, game_status.player.radius)


def draw_enemies():
    for enemy in game_status.enemies:
        pygame.draw.circle(game_status.screen, ENEMY_COLOR,
                           enemy.position.to_tuple(), ENEMY_RADIUS)


def draw_hearts():
    for heart in game_status.hearts:
        pygame.draw.circle(game_status.screen, HEART_COLOR,
                           heart.position.to_tuple(), HEART_RADIUS)


def draw_lives():
    font = pygame.font.Font(None, 50)
    lives_msg = font.render(
        "lives: " + str(game_status.player.lives), True, (220, 220, 220))
    game_status.screen.blit(lives_msg, (10, 10))


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

    game_status.player.player_pos_in_screen(PLAYER_RADIUS, game_status.screen_size[0] - PLAYER_RADIUS,
                                            PLAYER_RADIUS, game_status.screen_size[1] - PLAYER_RADIUS)


def check_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 用户点击左上角的退出
            game_status.running = False  # 设定游戏为终止状态


def draw():
    game_status.screen.fill(BG_COLOR)
    draw_player()
    draw_hearts()
    draw_enemies()
    draw_lives()
    pygame.display.update()  # 更新游戏界面


def update_hearts():
    obtained_hearts = [
        heart for heart in game_status.hearts if heart.is_player_collision(game_status.player)]
    game_status.hearts = [heart for heart in game_status.hearts if not
                          heart.is_player_collision(game_status.player)]  # order of these two lines of code matters

    for heart in obtained_hearts:
        game_status.player.add_lives(heart.lives)


def update_enemy():
    collided_enemies = [enemy for enemy in game_status.enemies
                        if enemy.is_player_collision(game_status.player)]
    game_status.enemies = [enemy for enemy in game_status.enemies if not
                           enemy.is_player_collision(game_status.player)]  # order of these two lines of code matters
    game_status.player.minus_lives(len(collided_enemies))


def update():
    update_player()
    update_hearts()
    update_enemy()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    first_game_setup()
    while game_status.running:
        check_event()
        update()
        draw()
