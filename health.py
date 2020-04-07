RED_HEART = 0
SOUL_HEART = 1
EVIL_HEART = 2

MAX_HEARTS = 24


class PlayerHealth:
    def __init__(self, *, heart_canisters=6, player):
        self.heart_canisters = heart_canisters
        self.health = heart_canisters
        self.extra_hearts = []
        self.player = player

    def heal(self, type):
        if type == RED_HEART:
            if self.health < self.heart_canisters:
                self.health += 1
            else:
                return False
        elif self.total_hearts() < MAX_HEARTS:
            self.extra_hearts.append(type)
        else:
            return False
        return True

    def damage(self):
        if not self.extra_hearts:
            self.health -= 1
            if self.health <= 0:
                self.player.kill()
        else:
            if self.extra_hearts.pop() == EVIL_HEART:
                self.player.game.enemy_damage(2 * self.player.shot_damage)

    def add_heart_canisters(self, amount):
        if self.heart_canisters == MAX_HEARTS:
            return
        self.heart_canisters += 1
        if self.total_hearts() > MAX_HEARTS:
            self.extra_hearts.pop()
        if amount > 1:
            self.add_heart_canisters(amount - 1)

    def total_hearts(self):
        return (self.heart_canisters + len(self.extra_hearts))
