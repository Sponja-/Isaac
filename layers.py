PLAYER = 0
PICKUPS = 1
ENEMIES = 2
OBSTACLES = 3
PLAYER_TEARS = 4
ENEMY_TEARS = 5
EXPLOSIONS = 6


collisions = {
    PLAYER: {
        PLAYER: False,
        PICKUPS: True,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: True,
        EXPLOSIONS: True
    },
    PICKUPS: {
        PLAYER: True,
        PICKUPS: True,
        ENEMIES: False,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False,
        EXPLOSIONS: True
    },
    ENEMIES: {
        PLAYER: True,
        PICKUPS: False,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: True,
        ENEMY_TEARS: False,
        EXPLOSIONS: True
    },
    OBSTACLES: {
        PLAYER: True,
        PICKUPS: True,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: True,
        ENEMY_TEARS: True,
        EXPLOSIONS: True
    },
    PLAYER_TEARS: {
        PLAYER: False,
        PICKUPS: False,
        ENEMIES: True,
        OBSTACLES: False,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False,
        EXPLOSIONS: False
    },
    ENEMY_TEARS: {
        PLAYER: True,
        PICKUPS: False,
        ENEMIES: False,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False,
        EXPLOSIONS: False
    },
    EXPLOSIONS: {
        PLAYER: True,
        PICKUPS: True,
        ENEMIES: True,
        OBSTACLES: True,
        PLAYER_TEARS: False,
        ENEMY_TEARS: False,
        EXPLOSIONS: False
    }
}
