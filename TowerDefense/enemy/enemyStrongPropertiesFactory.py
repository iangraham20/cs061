from interface import implements
from enemy.enemyPropertiesFactory import EnemyPropertiesFactory
from enemy.moveSlow import MoveSlow


class EnemyStrongPropertiesFactory(implements(EnemyPropertiesFactory)):
    def create_move_behavior(self):
        return MoveSlow()
