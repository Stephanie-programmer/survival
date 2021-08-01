import pygame

from utils import *

BG_COLOR = (0, 0, 0)
PLAYER_LENGTH = 70
PLAYER_POS_DIFF = 5

ENEMY_LENGTH = 50
HEART_LENGTH = 50

LIGHT_GREY = (220, 220, 220)
TOP_LEFT_CORNER = (10, 10)


def first_game_setup():
    pygame.init()
    pygame.display.set_caption("survival")
    game_status.running = True
    game_status.screen_size = (500, 500)
    game_status.screen = pygame.display.set_mode(game_status.screen_size)
    game_status.player_start_position = Position(250, 400)
    game_status.player = Player(
        position=game_status.player_start_position, lives=3, length=PLAYER_LENGTH)
    game_status.enemies = [Enemy(Position(100, 100), 1, ENEMY_LENGTH)]
    game_status.hearts = [Heart(Position(400, 400), HEART_LENGTH, 1)]
    load_images_to_game_status()


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


def draw():
    game_status.screen.fill(BG_COLOR)
    draw_player()
    draw_lives()
    draw_enemies()
    draw_hearts()
    pygame.display.update()


def draw_hearts():
    for heart in game_status.hearts:
        game_status.screen.blit(game_status.images["heart"], heart.position.to_tuple())


def draw_enemies():
    for enemy in game_status.enemies:
        game_status.screen.blit(game_status.images["enemy"], enemy.position.to_tuple())


def draw_lives():
    font = pygame.font.Font(None, 50)
    lives_msg = font.render("lives: " + str(game_status.player.lives), True, LIGHT_GREY)
    game_status.screen.blit(lives_msg, TOP_LEFT_CORNER)


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_status = GameStatus()
    first_game_setup()
    while game_status.running:
        check_event()
        update()
        draw()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
