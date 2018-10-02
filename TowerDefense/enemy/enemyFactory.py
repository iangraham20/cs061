class EnemyFactory:
    def create_enemy(self, canvas, path):
        raise NotImplementedError()

    def specify_enemy_type(self, canvas, path):
        enemy = self.create_enemy(canvas, path)   # ??
        enemy.set_properties()
        return enemy
