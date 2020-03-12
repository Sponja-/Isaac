PLAYER = 0
ITEMS = 1
ENEMIES = 2
OBSTACLES = 3
PLAYER_TEARS = 4
ENEMY_TEARS = 5


collisions = {
    PLAYER: {
        PLAYER: False,
        ITEMS: True,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: True
    },
    ITEMS: {
        PLAYER: True,
        ITEMS: True,
        ENEMIES: False,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False
    },
    ENEMIES: {
        PLAYER: True,
        ITEMS: False,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: True,
        ENEMY_TEARS: False
    },
    OBSTACLES: {
        PLAYER: True,
        ITEMS: True,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: True,
        ENEMY_TEARS: True
    },
    PLAYER_TEARS: {
        PLAYER: False,
        ITEMS: False,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False
    }
}
