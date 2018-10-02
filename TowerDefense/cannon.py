from projectile import *


class Cannon:
    def __init__(self, canvas, row, column, center):
        self._canvas = canvas
        self._row = row
        self._column = column
        self._center = center
        self._enemy_list = []
        self._target_type = 'first'
        self._target = None
        self._range = 20

    def fire_projectiles(self):
        if self._target:
            Projectile(self._canvas, self._center, self._target.get_center(), self._target)

    def set_target(self, target):
        self._target = target

    def get_target(self):
        return self._target

    def set_target_type(self, type):
        self._target_type = type

    def get_target_type(self):
        return self._target_type

    def get_center(self):
        return self._center

    def get_range(self):
        return self._range
