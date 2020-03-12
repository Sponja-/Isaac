class GameObject:
    to_kill = False
    sprite = None
    body = None

    def update(self, delta_time):
        pass

    def physics_update(self, delta_time):
        if self.body is not None:
            self.body.update(delta_time)

        if self.sprite is not None:
            if self.body is not None:
                point = self.body.collider.top_left()
                self.sprite.rect.x = int(point.x)
                self.sprite.rect.y = int(point.y)

    def on_collide(self, other):
        pass

    def on_kill(self):
        pass

    def kill(self, *args, **kwargs):
        self.to_kill = True
        self.kill_args = args
        self.kill_kwargs = kwargs
