class Enemy:

    @staticmethod
    def create_enemy(canvas, path, enemy_type):
        if enemy_type == "normal":
            from enemy.enemyNormalFactory import EnemyNormalFactory
            fact = EnemyNormalFactory()
        elif enemy_type == "strong":
            from enemy.enemyStrongFactory import EnemyStrongFactory
            fact = EnemyStrongFactory()
        elif enemy_type == "weak":
            from enemy.enemyWeakFactory import EnemyWeakFactory
            fact = EnemyWeakFactory()
        else:
            print("Don't have support for an enemy of type: " + enemy_type)
            return
        return fact.specify_enemy_type(canvas, path)

    def __init__(self, canvas, path):
        self._canvas = canvas
        self._path = path
        self._speed = 25
        self._destination_cell_index = 0
        self._destination_cell = self._path.get_cell(0)
        self._x, self._y = self._destination_cell.get_center()
        self._pathLength = len(self._path)
        self._compute_new_dir()
        self._id = None
        self._alive = True
        self._reached_goal = False
        self._is_moving = False
        self.moveBehavior = None
        self.color = None
        self.size = None
        self._health = 100
        # print("Enemy: (x, y) = ("+str(int(self._x))+", "+str(int(self._y))+")")

    def _compute_new_dir(self):
        self._destination_cell_index += 1
        self._destination_cell = self._path.get_cell(self._destination_cell_index)
        self.compute_direction_x()
        self.compute_direction_y()

    def compute_direction_x(self):
        distance_from_destination_x = self._destination_cell.get_center_x() - self._x
        if distance_from_destination_x > 0:
            self._direction_x = 1
        elif distance_from_destination_x == 0:
            self._direction_x = 0
        else:
            self._direction_x = -1

    def compute_direction_y(self):
        distance_from_destination_y = self._destination_cell.get_center_y() - self._y
        if distance_from_destination_y > 0:
            self._direction_y = 1
        elif distance_from_destination_y == 0:
            self._direction_y = 0
        else:
            self._direction_y = -1

    def move(self):
        if self._health <= 0:
            self._canvas.delete(self._id)
            self._alive = False
        elif self._destination_cell_index == self._pathLength - 1:
            self._canvas.delete(self._id)
            self._reached_goal = True
        else:
            if (self._x, self._y) == self._destination_cell.get_center():
                self._compute_new_dir()
            self.moveBehavior.move(self)
            self.render()
            self._canvas.after(self._speed, self.move)

    def is_off_screen(self):
        if (self._x < 0 or self._y < 0 or
                self._x > int(self._canvas.cget("width")) or
                self._y > int(self._canvas.cget('height'))):
            return True
        else:
            return False

    def start_moving(self):
        self._is_moving = True
        self.move()

    def decrease_health(self):
        self._health -= 25
        if self._health <= 0:
            self._alive = False

    def get_health(self):
        return self._health

    def get_direction_x(self):
        return self._direction_x

    def get_direction_y(self):
        return self._direction_y

    def update_x(self, x):
        self._x += x

    def update_y(self, y):
        self._y += y

    def get_center(self):
        return self._x, self._y

    def set_move_behavior(self, moveBehavior):
        self.moveBehavior = moveBehavior

    def is_alive(self):
        return self._alive

    def is_moving(self):
        return self._is_moving

    def reached_goal(self):
        return self._reached_goal

    def render(self):
        raise NotImplementedError("Must be implemented in subclass")

