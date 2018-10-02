from enemy.enemy import *


class Wave:
    def __init__(self, canvas, path, current_round, spawn_time):

        self._canvas = canvas
        self._path = path
        self._current_round = current_round
        self._spawn_time = spawn_time

        self._enemy_list = []
        self._enemies_in_wave = []
        self.set_enemies_in_wave()

        self._normal_enemies = int(self._enemies_in_wave[0])
        self._weak_enemies = int(self._enemies_in_wave[1])
        self._strong_enemies = int(self._enemies_in_wave[2])

        self._enemies_per_wave = self._normal_enemies + self._weak_enemies + self._strong_enemies
        self._next_enemy = 0
        self._spawned_enemy_objects = []
        self._wave_completed = False

        for i in range(self._weak_enemies):
            self._enemy_list.append(Enemy.create_enemy(self._canvas, self._path, "weak"))
        for i in range(self._normal_enemies):
            self._enemy_list.append(Enemy.create_enemy(self._canvas, self._path, "normal"))
        for i in range(self._strong_enemies):
            self._enemy_list.append(Enemy.create_enemy(self._canvas, self._path, "strong"))

    def update_wave_stats(self):
        if self._next_enemy < self._enemies_per_wave - 1:
            self.spawn()
            self._canvas.after(self._spawn_time, self.update_wave_stats)
        for enemy in self._enemy_list:
            if not enemy.is_alive():
                print("enemy died or reached goal")
                self._enemy_list.remove(enemy)

    def spawn(self):
        enemy = self._enemy_list[self._next_enemy]
        enemy.start_moving()
        self._spawned_enemy_objects.append(enemy)
        self._next_enemy += 1

    def get_enemy_list(self):
        return self._enemy_list

    def set_enemies_in_wave(self):
        if self._current_round <= 2:
            normal_enemies = self._current_round * 3 + 5
            weak_enemies = 0
            strong_enemies = 0
            self._enemies_in_wave.append(normal_enemies)
            self._enemies_in_wave.append(weak_enemies)
            self._enemies_in_wave.append(strong_enemies)
        elif self._current_round <= 4:
            normal_enemies = self._current_round * 3
            weak_enemies = self._current_round
            strong_enemies = 0
            self._enemies_in_wave.append(normal_enemies)
            self._enemies_in_wave.append(weak_enemies)
            self._enemies_in_wave.append(strong_enemies)
        elif self._current_round <= 6:
            normal_enemies = self._current_round * 3
            weak_enemies = self._current_round
            strong_enemies = self._current_round / 3
            self._enemies_in_wave.append(normal_enemies)
            self._enemies_in_wave.append(weak_enemies)
            self._enemies_in_wave.append(strong_enemies)
        elif self._current_round > 6:
            normal_enemies = self._current_round * 5
            weak_enemies = self._current_round * 3
            strong_enemies = self._current_round / 2
            self._enemies_in_wave.append(normal_enemies)
            self._enemies_in_wave.append(weak_enemies)
            self._enemies_in_wave.append(strong_enemies)
