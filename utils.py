class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y


class Player:
    def __init__(self, position, lives, length):
        self.position = position
        self.lives = lives
        self.length = length

    def update_position(self, position_diff):
        self.position.x += position_diff.x
        self.position.y += position_diff.y

    def add_lives(self, number_lives):
        self.lives += number_lives

    def minus_lives(self, number_lives):
        self.lives -= number_lives

    def restrict_in_screen(self, min_x, max_x, min_y, max_y):
        if self.position.x < min_x:
            self.position.x = min_x
        elif self.position.x > max_x:
            self.position.x = max_x
        if self.position.y < min_y:
            self.position.y = min_y
        elif self.position.y > max_y:
            self.position.y = max_y


class Enemy:
    def __init__(self, position, lives, length):
        self.position = position
        self.lives = lives
        self.length = length

    def is_player_collision(self, player):
        return abs(self.position.x - player.position.x) < (self.length) and abs(self.position.y - player.position.y) < (
            self.length)


class Heart:
    def __init__(self, position, length, lives):
        self.position = position
        self.lives = lives
        self.length = length

    def is_player_collision(self, player):
        return abs(self.position.x - player.position.x) < (self.length) and abs(self.position.y - player.position.y) < (
            self.length)


class GameStatus:
    def __init__(self):
        self.screen = None
        self.enemies = None
        self.hearts = None
        self.running = None
        self.screen_size = None
        self.player_start_position = None
        self.player = None
        self.images = None
        self.count_down = None
        self.pause = None
        self.level = None
        self.restart = None


ENEMY_LENGTH = 50
HEART_LENGTH = 50
PLAYER_LENGTH = 70


def get_current_level_data(current_level):
    levels = {
        1: {
            "hearts": [Heart(Position(400, 400), HEART_LENGTH, 1)],
            "enemies": [Enemy(Position(100, 100), 1, ENEMY_LENGTH)],
            "lives": 3,
            "count down": 10
        },
        2: {
            "hearts": [Heart(Position(400, 400), HEART_LENGTH, 1)],
            "enemies": [Enemy(Position(100, 100), 1, ENEMY_LENGTH), Enemy(Position(100, 400), 1, ENEMY_LENGTH)],
            "lives": 2,
            "count down": 15
        },
        3: {
            "hearts": [Heart(Position(400, 400), HEART_LENGTH, 1)],
            "enemies": [Enemy(Position(100, 100), 1, ENEMY_LENGTH), Enemy(Position(100, 400), 1, ENEMY_LENGTH),
                        Enemy(Position(200, 200), 1, ENEMY_LENGTH)],
            "lives": 1,
            "count down": 20
        }
    }
    current_level_data = levels[current_level]
    current_level_data["player"] = Player(position=Position(250, 400), lives=current_level_data["lives"],
                                          length=PLAYER_LENGTH)
    return current_level_data
