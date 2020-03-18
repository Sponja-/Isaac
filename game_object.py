from collections import OrderedDict


class GameObject:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.to_kill = False
        instance.body = None
        instance.sprite = None
        instance.on_mount = Event("mount")
        instance.on_update = Event("update")
        instance.on_physics_update = Event("physics_update")
        instance.on_collide = Event("collide")
        instance.on_kill = Event("kill")
        return instance

    def physics_update(self, delta_time):
        if self.body is not None:
            self.body.update(delta_time)

        if self.sprite is not None:
            if self.body is not None:
                point = self.body.collider.top_left()
                self.sprite.rect.x = int(point.x)
                self.sprite.rect.y = int(point.y)

        self.on_physics_update.dispatch(self, delta_time)

    def update(self, delta_time):
        self.pre_update(delta_time)
        self.on_update.dispatch(self, delta_time)
        self.post_update(delta_time)

    def pre_update(self, delta_time):
        pass

    def post_update(self, delta_time):
        pass

    def collide(self, other):
        self.on_collide.dispatch(self, other)

    def kill(self, *args, **kwargs):
        self.to_kill = True
        self.on_kill.dispatch(self, *args, **kwargs)


class Event:
    def __init__(self, name):
        self.handlers = OrderedDict()

    def __iadd__(self, handler):
        self.handlers[handler.__name__] = handler
        return self

    def remove(self, name):
        del self.handlers[name]

    def dispatch(self, *args, **kwargs):
        for name, handler in self.handlers.items():
            handler(*args, **kwargs)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        self.index += 1
        if self.index <= len(self.handlers):
            return self.handlers[self.index - 1]
