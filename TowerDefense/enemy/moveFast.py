from interface import implements
from enemy.moveBehavior import MoveBehavior


class MoveFast(implements(MoveBehavior)):
    def move(self, enemy):
        enemy.update_x(enemy.get_direction_x() * 2)
        enemy.update_y(enemy.get_direction_y() * 2)
