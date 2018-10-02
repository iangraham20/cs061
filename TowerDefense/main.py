'''
Tower Defense
Ian Christensen
igc2@students.calvin.ed
Professor Norman
Interim CS-W61-A
Winter 2018
'''

from tkinter import *
from path import *
from cell import *
from cellObserver import CellObserver
from cannon import *
from wave import *

CANVAS_SIZE = 500
SQUARE_PROP = 20
SQUARE_SIZE = int(CANVAS_SIZE / SQUARE_PROP)
ROUND_TIMER = 60
INIT_HEALTH = 100
INIT_MONEY = 100
INIT_ROUND = 0
INIT_KILLS = 0


class App(implements(CellObserver)):
    def __init__(self, root):
        self._root = root   # unsure what this is used for
        self._matrix = []
        self._waves = []
        self._targets = []
        self._cannons = []

        self._cannon_selection = None

        self._font = ("MV Boli", 10)
        self._padx = 0
        self._pady = 0

        self._round = INIT_ROUND
        self._kills = INIT_KILLS #TODO still needs implementation (should be for each cannon also...so add to cannon)
        self._money = INIT_MONEY
        self._health = INIT_HEALTH

        self._game_active = False
        self._read_path = True
        self._canvas = None

        self.initialize_game()

    def initialize_game(self):
        self.setup_board()
        self.prompt_user()

    def setup_board(self):
        self._canvas = Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self._canvas.pack()
        self.make_grid()
        self.read_path()

    def make_grid(self):
        for row in range(SQUARE_SIZE):
            cells = []
            for column in range(SQUARE_SIZE):
                cell = Cell(self._canvas, column, row, SQUARE_PROP)
                cell.register_observer(self)
                cells.append(cell)
            self._matrix.append(cells)

    def read_path(self):
        self._path = Path(SQUARE_SIZE)
        with open('path.txt') as file:
            self.generate_path(file)

    def generate_path(self, file):
        for coordinate in file:
            x, y = map(int, coordinate.strip().split(','))
            self._path.add_cell(self._matrix[y][x])
            self._matrix[y][x].set_type('path')

    def prompt_user(self):
        self._panel = Frame(root)
        self._panel.pack()
        self._button_start_game = Button(self._panel, text="Start Game", command=self.start_game, font=self._font)
        self._button_start_game.grid()

    def start_game(self):
        self._button_start_game.grid_forget()
        self.display_buttons()
        self.set_all_states(DISABLED)
        self.update_timer()
        self._game_active = True

    # this is for making your own path
    def write_path_info(self, cell):
        file = open('newpath.txt', 'a')
        file.write(str(cell.get_x()) + ", " + str(cell.get_y()) + "\n")
        cell.set_type('path')
        file.close()

    def display_buttons(self):
        self.display_game_options()
        self.display_cannon_options()
        self.display_target_options()
        self.display_player_statistics()

    def display_game_options(self):
        self._button_game_pause = Button(self._panel, text="Pause Game*", command=self.pause_game, padx=2, pady=2, font=self._font)
        self._button_game_pause.grid(row=0, column=0)
        self._button_game_speed = Button(self._panel, text="Fast Forward*", command=self.begin_round, padx=2, pady=2, font=self._font)
        self._button_game_speed.grid(row=1, column=0)
        self._button_begin_round = Button(self._panel, text="Start Round", command=self.begin_round, padx=2, pady=2, font=self._font)
        self._button_begin_round.grid(row=2, column=0)

    def display_cannon_options(self):
        self._button_cannon_heavy = Button(self._panel, text="Heavy", command=None, padx=self._padx, pady=self._pady, font=self._font)
        self._button_cannon_heavy.grid(row=1, column=4)
        self._button_cannon_light = Button(self._panel, text="Light", command=None, padx=self._padx, pady=self._pady, font=self._font)
        self._button_cannon_light.grid(row=2, column=4)
        self._button_cannon_ranged = Button(self._panel, text="Ranged", command=None, padx=self._padx, pady=self._pady, font=self._font)
        self._button_cannon_ranged.grid(row=1, column=3)
        self._button_cannon_double = Button(self._panel, text="Double", command=None, padx=self._padx, pady=self._pady, font=self._font)
        self._button_cannon_double.grid(row=2, column=3)

    def display_target_options(self):
        self._button_target_first = Button(self._panel, text="First", command=self.set_first, padx=self._padx, pady=self._pady, font=self._font)
        self._button_target_first.grid(row=1, column=8)
        self._button_target_last = Button(self._panel, text="Last", command=self.set_last, padx=self._padx, pady=self._pady, font=self._font)
        self._button_target_last.grid(row=2, column=8)
        self._button_target_strongest = Button(self._panel, text="Strongest", command=self.set_strongest, padx=self._padx, pady=self._pady, font=self._font)
        self._button_target_strongest.grid(row=1, column=7)
        self._button_target_weakest = Button(self._panel, text="Weakest", command=self.set_weakest, padx=self._padx, pady=self._pady, font=self._font)
        self._button_target_weakest.grid(row=2, column=7)

    def display_player_statistics(self):
        self.display_header()
        self.display_health()
        self.display_money()
        self.display_round()
        self.display_timer()

    def display_header(self):
        Label(self._panel, text="Upgrades: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=0, column=3, sticky=W)
        Label(self._panel, text="Stats: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=0, column=5, sticky=W)
        Label(self._panel, text="Target: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=0, column=7, sticky=W)

    def display_round(self):
        Label(self._panel, text="Round: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=2, column=1, sticky=W)
        self._variable_round = IntVar()
        self._variable_round.set(INIT_ROUND)
        self._label_round = Label(self._panel, textvariable=self._variable_round, padx=self._padx, pady=self._pady, font=self._font)
        self._label_round.grid(row=2, column=2)

    def display_timer(self):
        Label(self._panel, text="Next Round: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=1, column=1)
        self._variable_timer = IntVar()
        self._variable_timer.set(ROUND_TIMER)
        self._label_timer = Label(self._panel, textvariable=self._variable_timer, padx=self._padx, pady=self._pady, font=self._font)
        self._label_timer.grid(row=1, column=2)

    def display_health(self):
        Label(self._panel, text="Health: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=2, column=5)
        self._variable_health = IntVar()
        self._variable_health.set(INIT_HEALTH)
        self._label_health = Label(self._panel, textvariable=self._variable_health, padx=self._padx, pady=self._pady, font=self._font)
        self._label_health.grid(row=2, column=6)

    def display_money(self):
        Label(self._panel, text="Money: ", padx=self._padx, pady=self._pady, font=self._font).grid(row=1, column=5)
        self._variable_money = IntVar()
        self._variable_money.set(INIT_MONEY)
        self._label_money = Label(self._panel, textvariable=self._variable_money, padx=self._padx, pady=self._pady, font=self._font)
        self._label_money.grid(row=1, column=6)

    def set_all_states(self, state):
        self.set_cannon_states(state)
        self.set_target_states(state)

    def set_target_states(self, state):
        self._button_target_first.config(state=state)
        self._button_target_last.config(state=state)
        self._button_target_strongest.config(state=state)
        self._button_target_weakest.config(state=state)

    def set_cannon_states(self, state):
        self._button_cannon_heavy.config(state=state)
        self._button_cannon_light.config(state=state)
        self._button_cannon_ranged.config(state=state)
        self._button_cannon_double.config(state=state)

    def end_game(self):
        self.reset_statistics()
        self.set_all_states(DISABLED)
        # TODO add a game over screen that gives stats before resetting the board (leaderboard???)

    def reset_statistics(self):
        self._round = INIT_ROUND
        self._kills = INIT_KILLS
        self._money = INIT_MONEY
        self._health = INIT_HEALTH
        self._game_active = False

    def update_timer(self):
        time_left = self._variable_timer.get() - 1
        self._variable_timer.set(time_left)
        self.check_timer(time_left)
        self._canvas.after(1000, self.update_timer)

    def check_timer(self, time_left):
        if time_left < 0:
            self.begin_round()
            print("Timer reached zero...")

    def begin_round(self):
        if self._health <= 0:
            self.end_game()
        self.update_round_variables()
        self.create_enemy_wave(self._round)
        print("Beginning new round...\nResetting the timer...")

    def update_round_variables(self):
        self._round += 1
        self._variable_round.set(self._round)
        self._variable_timer.set(ROUND_TIMER)

    def update(self, cell):
        if not self._game_active: # is there a better way to check for the game running???
            return
        elif self._read_path:
            self.handle_click(cell)
        else:
            self.write_path_info(cell)  # is there a better way to handle this???

    def handle_click(self, cell):
        if cell.get_type() == 'other':
            self.purchase_cannon(cell)
        elif cell.get_type() == 'cannon':
            for cannon in self._cannons:
                if cell.get_center() == cannon.get_center():
                    self._cannon_selection = cannon
            self.cannon_properties()
        elif cell.get_type() == 'path':
            return
        else:
            print("some kind of error")
        print('A cell of type "'+str(cell.get_type())+'" was clicked on')

    def purchase_cannon(self, cell):
        if self._money >= 25:
            self._money -= 25
            self._variable_money.set(self._money)
            self.place_cannon(cell)

    def place_cannon(self, cell):
        cell.set_type('cannon')
        cannon = Cannon(self._canvas, cell.get_y(), cell.get_x(), cell.get_center())
        self._cannons.append(cannon)
        self.target_enemies(cannon)
        print('Cannon #' + str(len(self._cannons)) +
              " was placed at coordinates: " + str(cell.get_x()) + ", " + str(cell.get_y()))

    def target_enemies(self, cannon):
        self.update_targets()
        self.assign_target(cannon)
        cannon.fire_projectiles()
        self._canvas.after(500, self.target_enemies, cannon)

    def update_targets(self):
        for target in self._targets:
            if not target.is_alive():
                self._targets.remove(target)
                self._money += 25
                self._variable_money.set(self._money)
            if target.reached_goal():   # TODO should be updated regardless of whether there is a cannon shooting...
                print("lost 5 health!")
                self._targets.remove(target)
                self._health -= 5
                self._variable_health.set(self._health)

    # this whole method sucks as far as runtime goes...
    def assign_target(self, cannon):
        first = None
        last = None
        strongest = None
        weakest = None
        for enemy in self._targets:
            if enemy.is_alive() and enemy.is_moving() and self.distance(enemy, cannon) < 100:
                first = enemy
                break
        for enemy in reversed(self._targets):
            if enemy.is_alive() and enemy.is_moving():
                last = enemy
                break
        for enemy in self._targets:
            if enemy.is_alive() and enemy.is_moving():
                if not strongest:
                    strongest = enemy
                if enemy.get_health() > strongest.get_health():
                    strongest = enemy
        for enemy in self._targets:
            if enemy.is_alive() and enemy.is_moving():
                if not weakest:
                    weakest = enemy
                if enemy.get_health() < weakest.get_health():
                    weakest = enemy
        if first == None:
            cannon.set_target(None)
        elif not self._targets:
            cannon.set_target(None)
        elif cannon.get_target_type() == 'first':
            cannon.set_target(first)
        elif cannon.get_target_type() == 'last':
            cannon.set_target(last)
        elif cannon.get_target_type() == 'strongest':
            cannon.set_target(strongest)
        elif cannon.get_target_type() == 'weakest':
            cannon.set_target(weakest)

    def set_target(self, target):
        self._cannon_selection.set_target_type(target)

    def set_first(self):
        self.set_target('first')

    def set_last(self):
        self.set_target('last')

    def set_strongest(self):
        self.set_target('strongest')

    def set_weakest(self):
        self.set_target('weakest')

    def cannon_properties(self):
        self.set_all_states(NORMAL)

    def create_enemy_wave(self, current_round):
        print("Creating enemy wave # " + str(len(self._waves) + 1))
        wave = Wave(self._canvas, self._path, current_round, 1000)
        for enemy in wave.get_enemy_list():
            self._targets.append(enemy)
        self._waves.append(wave)
        wave.update_wave_stats()
        self._wave_active = True

    def pause_game(self):
        self._canvas.after(1000)

    def distance(self, enemy, cannon):
        return math.sqrt(((cannon.get_center()[0] - enemy.get_center()[0]) ** 2) + ((cannon.get_center()[1] - enemy.get_center()[1]) ** 2))


root = Tk()
root.title("Tower Defense")
App(root)
root.resizable(width=False, height=False)
root.wm_attributes('-topmost', 1)
root.mainloop()
