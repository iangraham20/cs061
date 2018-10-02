from enemy.enemy import Enemy


class EnemyStrong(Enemy):
    def __init__(self, enemyPropertiesFactory, canvas, path):
        Enemy.__init__(self, canvas, path)
        self._enemyPropertiesFactory = enemyPropertiesFactory

    def set_properties(self):
        self.set_move_behavior(self._enemyPropertiesFactory.create_move_behavior())
        self.color = "black"
        self.size = 7
        self.health = 100 # should be strong...

    def render(self):
        self._canvas.delete(self._id)
        self._id = self._canvas.create_oval(self._x - self.size, self._y - self.size,
                                    self._x + self.size, self._y + self.size,
                                    fill = self.color)
