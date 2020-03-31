import pygame as pg
from game_object import GameObject, Event
from physics import RigidBody, Vector, CircleCollider
from debug_sprites import CircleSprite,  colors
from tears import PlayerTear
import layers

SQRT_2 = 2 ** .5
INVULNERABLE_TIME = 1


class Player(GameObject):
    def __init__(self, *, position):
        self.body = RigidBody(collider=CircleCollider,
                              position=position,
                              radius=20,
                              damping=3.5)

        self.sprite = CircleSprite(colors.BLACK, self.body.collider.radius)
        self.layer = layers.PLAYER

        # Stats
        self.stats = {
            "Speed": 1000,
            "Damage": 50,
            "Shot Speed": 300,
            "Range": 600,
            "Tears": 10,
            "Max Health": 3
        }

        self.pickups = {
            "Coins": 0,
            "Bombs": 0,
            "Keys": 0
        }

        self.on_move = Event("move")
        self.on_fire = Event("fire")
        self.on_heal = Event("heal")
        self.on_stat_change = Event("stat_change")
        self.on_damage = Event("damage")
        self.on_enemy_kill = Event("enemy_kill")
        self.on_acquire_item = Event("acquire_item")

        self.on_update += register_keys
        self.on_update += move
        self.on_update += fire

        self.health = 3
        self.can_shoot = True
        self.invulnerable = False
        self.items = []

    def damage(self, amount=.5):
        if self.invulnerable:
            return False

        self.health -= amount
        self.invulnerable = True

        def reset_invulnerable():
            self.invulnerable = False

        self.game.add_timer(INVULNERABLE_TIME, reset_invulnerable)

        self.on_damage.dispatch(self, amount)

        if self.health <= 0:
            self.kill()

        print(self.health)

        return True

    def heal(self, amount):
        if self.health + amount > self.stats["Max Health"]:
            self.health = self.stats["Max Health"]
        else:
            self.health += amount

        self.on_heal.dispatch(self, amount)

    def set_stat(self, name, amount, *, mode="set"):
        prev = self.stats[name]

        if mode == "set":
            self.stats[name] = amount
        elif mode == "add":
            self.stats[name] += amount

        self.on_stat_change.dispatch(self, name, prev, self.stats[name])

    def acquire_item(self, item):
        self.items.append(item)
        item.on_pickup(self)


def register_keys(self, delta_time):
    keys = pg.key.get_pressed()
    self.keys = {}
    self.keys['w'] = keys[pg.K_w]
    self.keys['a'] = keys[pg.K_a]
    self.keys['s'] = keys[pg.K_s]
    self.keys['d'] = keys[pg.K_d]
    self.keys["up"] = keys[pg.K_UP]
    self.keys["down"] = keys[pg.K_DOWN]
    self.keys["left"] = keys[pg.K_LEFT]
    self.keys["right"] = keys[pg.K_RIGHT]
    self.keys["q"] = keys[pg.K_q]
    self.keys["space"] = keys[pg.K_SPACE]


def move(self, delta_time):
    movement_axes = 0
    move_force = Vector(0, 0)
    speed = self.stats["Speed"]

    if self.keys['w']:
        movement_axes += 1
        move_force += (0, -speed)
    elif self.keys['s']:
        movement_axes += 1
        move_force += (0, speed)
    if self.keys['a']:
        movement_axes += 1
        move_force += (-speed, 0)
    elif self.keys['d']:
        movement_axes += 1
        move_force += (speed, 0)

    if movement_axes == 2:
        move_force /= SQRT_2

    if movement_axes:
        self.body.add_force(move_force)
        self.on_move.dispatch(self, delta_time)


def fire(self, delta_time):
    if not self.can_shoot:
        return

    shot_speed = self.stats["Shot Speed"]
    player_v = self.body.velocity / 300
    if self.keys["up"]:
        velocity = Vector(0, -1) + (player_v.x, 0)
    elif self.keys["down"]:
        velocity = Vector(0, 1) + (player_v.x, 0)
    elif self.keys["left"]:
        velocity = Vector(-1, 0) + (0, player_v.y)
    elif self.keys["right"]:
        velocity = Vector(1, 0) + (0, player_v.y)
    else:
        return

    velocity.normalize()
    velocity *= shot_speed

    tear = PlayerTear(position=self.body.collider.center(),
                      velocity=velocity,
                      range=self.stats["Range"],
                      damage=self.stats["Damage"])
    self.game.add(tear)
    self.can_shoot = False

    def reset_shoot():
        self.can_shoot = True

    self.game.add_timer(self.stats["Tears"] / 10, reset_shoot)

    self.on_fire.dispatch(self, tear)
