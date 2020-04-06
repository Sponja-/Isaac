RED_HEART = 0
HALF_HEART = 1
SOUL_HEART = 2
EVIL_HEART = 3
HALF_SOUL = 4
HALF_EVIL = 5
DOUBLE_HEART = 6

MAX_HEARTS = 12

amounts = {
    RED_HEART: 1,
    HALF_HEART: .5,
    DOUBLE_HEART: 2
}


half_version = {
    SOUL_HEART: HALF_SOUL,
    EVIL_HEART: HALF_EVIL
}


full_version = {
    HALF_SOUL: SOUL_HEART,
    HALF_EVIL: EVIL_HEART
}


class PlayerHealth:
    def __init__(self, *, heart_canisters=3, player):
        self.heart_canisters = heart_canisters
        self.health = heart_canisters
        self.extra_hearts = []
        self.player = player

    def heal(self, type):
        if self.total_hearts() >= MAX_HEARTS:
            return False
        if type in (RED_HEART, HALF_HEART, DOUBLE_HEART):
            if self.health < self.heart_canisters:
                self.health += amounts[type]
                if self.health > self.heart_canisters:
                    self.health = self.heart_canisters
            else:
                return False
        elif type in half_version.keys():  # Is full heart?
            if self.extra_hearts[-1] in full_version.keys():
                if self.extra_hearts[-1] == half_version[type]:
                    self.extra_hearts.insert(-1, type)
                else:
                    half = self.extra_hearts.pop()
                    self.extra_hearts.append(full_version[half])
                    self.extra_hearts.append(half_version[type])
        elif type in full_version.keys():  # Is half heart?
            if self.extra_hearts[-1] in full_version.keys():
                self.extra_hearts.append(full_version[self.extra_hearts.pop()])
            else:
                self.extra_hearts.append(type)
        if self.total_hearts() >= MAX_HEARTS:
            assert(self.extra_hearts[-1] in full_version.keys())
            self.extra_hearts.pop()
        return True

    def damage(self, amount=.5):
        if not self.extra_hearts:
            self.health -= amount
            if self.health <= 0:
                self.player.kill()
        else:
            lost_heart = None
            if amount == .5:
                if self.extra_hearts[-1] in full_version.keys():
                    lost_heart = self.extra_hearts.pop()
                else:
                    self.extra_hearts.append(half_version[self.extra_hearts.pop()])
            elif amount == 1:
                if self.extra_hearts[-1] in full_version.keys():
                    lost_heart = self.extra_hearts.pop()
                    self.extra_hearts.append(half_version[self.extra_hearts.pop()])
                else:
                    lost_heart = self.extra_hearts.pop()
            else:
                self.damage(1)
                self.damage(amount - 1)
            if lost_heart in (HALF_EVIL, EVIL_HEART):
                self.player.game.enemy_damage(2 * self.player.stats["Damage"])

    def add_heart_canisters(self, amount):
        if self.heart_canisters == MAX_HEARTS:
            return
        self.heart_canisters += 1
        if self.total_hearts() <= MAX_HEARTS:
            return
        else:
            self.extra_hearts[-1].pop()
        if amount > 1:
            self.add_heart_canisters(amount - 1)

    def total_hearts(self):
        return (self.heart_canisters + len(self.extra_hearts)
                - (0.5 if self.extra_hearts and self.extra_hearts[-1] in full_version.keys() else 0))
