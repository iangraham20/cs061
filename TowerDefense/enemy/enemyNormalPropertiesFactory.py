from interface import implements
from enemy.enemyPropertiesFactory import EnemyPropertiesFactory
from enemy.moveNormal import MoveNormal


class EnemyNormalPropertiesFactory(implements(EnemyPropertiesFactory)):
    def create_move_behavior(self):
        return MoveNormal()
