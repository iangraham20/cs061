import random
import math


class Projectile:
    def __init__(self, canvas, origin, target, enemy):
        self._enemy = enemy
        self._canvas = canvas
        self._origin = origin
        self._x = origin[0]
        self._y = origin[1]
        self._target = target
        self._targetx = target[0]
        self._targety = target[1]
        self._size = 2
        self._angle = self.calculate_angle()
        self._dx = -7 * math.cos(self._angle)
        self._dy = -7 * math.sin(self._angle)
        self._speed = 15
        self._id = None
        self.render()
        self.calculate_angle()

    def get_center(self):
        return self._x, self._y

    def calculate_angle(self):
        randomness = random.uniform(-.02, .02)
        x = self._x - self._targetx
        y = self._y - self._targety
        angle = math.atan2(y, x)
        angle += randomness
        return angle

    def move(self):
        self._x += self._dx
        self._y += self._dy

    def is_off_canvas(self):
        if (self._x < 0 or self._y < 0 or
                self._x > int(self._canvas.cget("width")) or
                self._y > int(self._canvas.cget('height'))):
            return True
        else:
            return False

    def get_distance(self):
        return math.sqrt(((self._x - self._enemy.get_center()[0]) ** 2) + ((self._y - self._enemy.get_center()[1]) ** 2))

    def is_collision(self):
        if self.get_distance() < 10:
            # print("the projectile hit the target!")
            self._enemy.decrease_health()
            return True
        else:
            # print("the projectile missed the target!")
            return False

    def render(self):
        self._canvas.delete(self._id)
        if not self.is_off_canvas() and not self.is_collision():
            self.move()
            self._id = self._canvas.create_oval(self._x - self._size, self._y - self._size,
                                                self._x + self._size, self._y + self._size,
                                                fill="grey", outline="black")
            self._canvas.after(60, self.render)
