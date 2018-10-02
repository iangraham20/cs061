from interface import implements
from enemy.enemyPropertiesFactory import EnemyPropertiesFactory
from enemy.moveFast import MoveFast


class EnemyWeakPropertiesFactory(implements(EnemyPropertiesFactory)):
    def create_move_behavior(self):
        return MoveFast()
