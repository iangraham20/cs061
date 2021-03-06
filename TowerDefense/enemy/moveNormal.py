from interface import implements
from enemy.moveBehavior import MoveBehavior


class MoveNormal(implements(MoveBehavior)):
    def move(self, enemy):
        enemy.update_x(enemy.get_direction_x())
        enemy.update_y(enemy.get_direction_y())
