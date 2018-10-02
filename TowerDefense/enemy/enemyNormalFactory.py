from enemy.enemyFactory import EnemyFactory
from enemy.enemyStrongPropertiesFactory import EnemyStrongPropertiesFactory
from enemy.enemyNormal import EnemyNormal


class EnemyNormalFactory(EnemyFactory):
    def create_enemy(self, canvas, path):
        properties_factory = EnemyStrongPropertiesFactory()
        return EnemyNormal(properties_factory, canvas, path)
