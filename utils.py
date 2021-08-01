class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)


class Player:
    def __init__(self, position, lives, radius):
        self.position = position
        self.lives = lives
        self.radius = radius

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
    def __init__(self, position, lives, radius):
        self.position = position
        self.lives = lives
        self.radius = radius

    def is_player_collision(self, player):
        return (self.position.x - player.position.x) ** 2 + (self.position.y - player.position.y) ** 2 < (
                self.radius + player.radius) ** 2


class Heart:
    def __init__(self, position, radius, lives):
        self.position = position
        self.lives = lives
        self.radius = radius

    def is_player_collision(self, player):
        return (self.position.x - player.position.x) ** 2 + (self.position.y - player.position.y) ** 2 < (
                self.radius + player.radius) ** 2


class GameStatus:
    def __init__(self):
        self.screen = None
        self.enemies = None
        self.hearts = None
        self.running = None
        self.screen_size = None
        self.player_start_position = None
        self.player = None
