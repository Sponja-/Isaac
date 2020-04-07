import pygame as pg
from game_object import GameObject, Event
from physics import RigidBody, Vector, CircleCollider
from debug_sprites import CircleSprite,  colors
from health import PlayerHealth
from tears import PlayerTear
from bombs import PlacedBomb
import layers

SQRT_2 = 2 ** .5
INVULNERABLE_TIME = 1


class PlayerStat:
    def __init__(self, name, *, start_val=None):
        self.name = name
        self.value = start_val

    def __get__(self, player, _):
        return self.value

    def __set__(self, player, value):
        old_val = self.value
        self.value = value
        player.on_stat_change.dispatch(player, self.name, old_val, value)


pickups = ["coins", "bombs", "keys"]


class Player(GameObject):
    coins = PlayerStat("coins", start_val=0)
    bombs = PlayerStat("bombs", start_val=1)
    keys = PlayerStat("keys", start_val=0)
    speed = PlayerStat("speed", start_val=1000)
    shot_damage = PlayerStat("shot_damage", start_val=50)
    shot_speed = PlayerStat("shot_speed", start_val=300)
    range = PlayerStat("range", start_val=600)
    tears = PlayerStat("tears", start_val=10)

    def __init__(self, *, position):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=20,
                              damping=3.5,
                              is_player=True)

        self.sprite = CircleSprite(colors.BLACK, self.body.collider.radius)
        self.layer = layers.PLAYER

        self.on_move = Event("move")
        self.on_fire = Event("fire")
        self.on_heal = Event("heal")
        self.on_damage = Event("damage")
        self.on_enemy_kill = Event("enemy_kill")
        self.on_acquire_item = Event("acquire_item")
        self.on_stat_change = Event("stat_change")

        self.on_update += register_keys
        self.on_update += move
        self.on_update += fire
        self.on_update += bomb_place

        self.on_stat_change += update_pickups

        self.health = PlayerHealth(heart_canisters=3,
                                   player=self)
        self.can_shoot = True
        self.can_place_bomb = True
        self.invulnerable = False
        self.items = []

    def damage(self, amount=.5):
        stop_damage = self.on_damage.dispatch(self, amount)

        if self.invulnerable or any(stop_damage):
            return False

        self.health.damage(amount)
        self.invulnerable = True

        def reset_invulnerable():
            self.invulnerable = False

        self.game.add_timer(INVULNERABLE_TIME, reset_invulnerable)

        return True

    def heal(self, type):
        if self.health.heal(type):
            self.on_heal.dispatch(self, type)
            return True
        return False

    def add_hearts(self, amount):
        self.health.add_heart_canisters(amount)

    def acquire_item(self, item):
        self.items.append(item)
        item.on_pickup(self)


def register_keys(self, delta_time):
    keys = pg.key.get_pressed()
    self.pressed_keys = {}
    self.pressed_keys['w'] = keys[pg.K_w]
    self.pressed_keys['a'] = keys[pg.K_a]
    self.pressed_keys['s'] = keys[pg.K_s]
    self.pressed_keys['d'] = keys[pg.K_d]
    self.pressed_keys["up"] = keys[pg.K_UP]
    self.pressed_keys["down"] = keys[pg.K_DOWN]
    self.pressed_keys["left"] = keys[pg.K_LEFT]
    self.pressed_keys["right"] = keys[pg.K_RIGHT]
    self.pressed_keys["q"] = keys[pg.K_q]
    self.pressed_keys["e"] = keys[pg.K_e]
    self.pressed_keys["space"] = keys[pg.K_SPACE]


def move(self, delta_time):
    movement_axes = 0
    move_force = Vector(0, 0)

    if self.pressed_keys['w']:
        movement_axes += 1
        move_force += (0, -self.speed)
    elif self.pressed_keys['s']:
        movement_axes += 1
        move_force += (0, self.speed)
    if self.pressed_keys['a']:
        movement_axes += 1
        move_force += (-self.speed, 0)
    elif self.pressed_keys['d']:
        movement_axes += 1
        move_force += (self.speed, 0)

    if movement_axes == 2:
        move_force /= SQRT_2

    if movement_axes:
        self.body.add_force(move_force)
        self.on_move.dispatch(self, delta_time)


def fire(self, delta_time):
    if not self.can_shoot:
        return

    player_v = self.body.velocity / 300
    if self.pressed_keys["up"]:
        velocity = Vector(0, -1) + (player_v.x, 0)
    elif self.pressed_keys["down"]:
        velocity = Vector(0, 1) + (player_v.x, 0)
    elif self.pressed_keys["left"]:
        velocity = Vector(-1, 0) + (0, player_v.y)
    elif self.pressed_keys["right"]:
        velocity = Vector(1, 0) + (0, player_v.y)
    else:
        return

    velocity.normalize()
    velocity *= self.shot_speed

    tear = PlayerTear(position=self.body.collider.center(),
                      velocity=velocity,
                      range=self.range,
                      damage=self.shot_damage)
    self.game.add(tear)
    self.can_shoot = False

    def reset_shoot():
        self.can_shoot = True

    self.game.add_timer(self.tears / 10, reset_shoot)

    self.on_fire.dispatch(self, tear)


def bomb_place(self, delta_time):
    if self.can_place_bomb and self.pressed_keys['e'] and self.bombs > 0:
        self.can_place_bomb = False
        self.bombs -= 1

        def reset_bomb_place():
            self.can_place_bomb = True

        self.game.add_timer(3, reset_bomb_place)

        self.game.add(PlacedBomb(position=self.body.collider.center()))


def update_pickups(self, stat_name, *_):
    if stat_name in pickups:
        data = {}
        for name in pickups:
            data[name] = getattr(self, name)

        self.game.ui_objects["pickups"].set_stats(data)
