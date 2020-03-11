class GameObject:

    def update(self, delta_time):
        pass

    def physics_update(self, delta_time):
        if self.body is not None:
            self.body.update(delta_time)

        if self.sprite is not None:
            if self.body is not None:
                self.sprite.rect.x = int(self.body.position.x)
                self.sprite.rect.y = int(self.body.position.y)

    def on_collide(self, other):
        pass
