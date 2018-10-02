from enemy.enemyFactory import EnemyFactory
from enemy.enemyWeakPropertiesFactory import EnemyWeakPropertiesFactory
from enemy.enemyWeak import EnemyWeak


class EnemyWeakFactory(EnemyFactory):
    def create_enemy(self, canvas, path):
        properties_factory = EnemyWeakPropertiesFactory()
        return EnemyWeak(properties_factory, canvas, path)
