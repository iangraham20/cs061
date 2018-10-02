from enemy.enemyFactory import EnemyFactory
from enemy.enemyStrongPropertiesFactory import EnemyStrongPropertiesFactory
from enemy.enemyStrong import EnemyStrong


class EnemyStrongFactory(EnemyFactory):
    def create_enemy(self, canvas, path):
        properties_factory = EnemyStrongPropertiesFactory()
        return EnemyStrong(properties_factory, canvas, path)
