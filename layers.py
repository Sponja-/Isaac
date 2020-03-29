PLAYER = 0
PICKUPS = 1
ENEMIES = 2
OBSTACLES = 3
PLAYER_TEARS = 4
ENEMY_TEARS = 5
FLYING_ENEMIES = 6


collisions = {
    PLAYER: {
        PLAYER: False,
        PICKUPS: True,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: True
    },
    PICKUPS: {
        PLAYER: True,
        PICKUPS: True,
        ENEMIES: False,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False
    },
    ENEMIES: {
        PLAYER: True,
        PICKUPS: False,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: True,
        ENEMY_TEARS: False
    },
    OBSTACLES: {
        PLAYER: True,
        PICKUPS: True,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: True,
        ENEMY_TEARS: True
    },
    PLAYER_TEARS: {
        PLAYER: False,
        PICKUPS: False,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False
    }
}
