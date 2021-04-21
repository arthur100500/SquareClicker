from square import BlueSquare, RedSquare, GreenSquare, GraySquare, OrangeSquare, StartSquare, BackgroundSquare, RetrySquare, play_sound, GameOverSquare
from misc import BaseSprite
import pygame

# constants
BACKGROUND_TEXTURE = "playfield26x.png"
GRAY_SQUARE_TEXTURE = "graysquare6x.png"
GREEN_SQUARE_TEXTURE = "greensquare6x.png"
RED_SQUARE_TEXTURE = "redsquare6x.png"
BLUE_SQUARE_TEXTURE = "bluesquare6x.png"
START_SQUARE_TEXTURE = "start6x.png"
BG_SQUARE_TEXTURE = "transparentpixel.png"
RETRY_SQUARE_TEXTURE = "retry6x.png"
GAMEOVER_SQUARE_TEXTURE = "gameover6x.png"


class Game:
    def __init__(self, size, sprite_group, self_playing=False):
        from time import time
        self.grid = Grid(self)
        self.score = 0
        self.auto = self_playing
        self.time = 10
        self.initial_time = 10
        self.last_tick_time = time()
        self.state = "not started"
        self.combo = 0
        self.time_multiplier = 3
        self.grid_size = 19 * 6
        self.window_size = size
        self.squares_to_draw = []
        self.sprite_group = sprite_group
        self.change_state = True
        self.health_points = 1

    def on_click(self, x, y):
        cell = self.detect_cell(x, y)
        if cell:
            self.grid.click_cell(cell)
            if cell != "no cell":
                self.grid.test(cell)
        self.print_state()

    def detect_cell(self, x, y):
        y = self.window_size[1] - y
        for i in range(3 * 6, self.window_size[0], self.grid_size):
            for j in range(3 * 6, self.window_size[0], self.grid_size):
                if (i < x < i + self.grid_size - 3 * 6) and (j < y < j + self.grid_size - 3 * 6):
                    return list(map(int, [(i - 6 * 3) / self.grid_size, (j - 6 * 3) / self.grid_size]))
        return "no cell"

    def begin(self):
        self.grid.init_start_button()

    def show_retry_screen(self):
        self.grid.init_retry_screen()

    def start(self):
        self.grid = Grid(self)
        self.time = self.initial_time
        self.score = 0
        self.combo = 0
        self.state = "running"
        play_sound("startsound.mp3")

    def tick(self):
        from time import time
        # render
        self.draw_squares(self.sprite_group)
        if self.state == "over":
            self.last_tick_time = time()
            return
        # time checking
        if self.state == "running":
            self.time -= (time() - self.last_tick_time)
            self.time = min(self.time, 1.3 * self.initial_time)
        self.last_tick_time = time()
        self.health_points = self.time / self.initial_time
        # if lost
        if self.time < 0:
            # defeat
            time = 10
            import square
            square.play_sound("zvukiprajeniya.mp3")
            self.show_retry_screen()
            self.state = "over"
            return
        # try to generate grid
        x = -1
        y = -1
        # click grid if auto
        if self.auto:
            for elem in self.grid.grid:
                y += 1
                for elem2 in elem:
                    x += 1
                    if elem2.__class__ == GreenSquare or elem2.__class__ == BlueSquare:
                        self.grid.click_cell([x, y])
                        self.grid.test([x, y])
                        print(x, y)
                x = -1

        self.grid.try_to_generate()

    def print_state(self):
        print("Game ", self.state, self.combo, int(self.score), int(self.time))

    def print_grid(self):
        for line in self.grid.grid:
            print(line[0], line[1], line[2], line[3], line[4])
        print()

    def draw_health(self, screen):
        x = min(self.health_points, 1)
        if int(self.health_points * 588) > 0:
            pygame.draw.rect(screen, (int(255 * (abs(x - 1) - abs(x - 0.5) + 0.5)), int(255 * (1 - (abs(x - 0.5) - abs(x) + 0.5))), 0), (0, 0, int(self.health_points * 588), 12))

    def draw_squares(self, sprite_group):
        square_list = self.grid.get_squares()
        for elem in square_list:
            coords = [0, 0]
            elem[0] = 4 - elem[0]
            elem[1] = 4 - elem[1]
            elem[1], elem[0] = elem[0], elem[1]
            coords[0] = self.window_size[0] - ((elem[0] + 1) * 19 * 6)
            coords[1] = self.window_size[1] - (elem[1] + 1) * 19 * 6
            if elem[2].__class__ == GreenSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, GREEN_SQUARE_TEXTURE))
            elif elem[2].__class__ == RedSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, RED_SQUARE_TEXTURE))
            elif elem[2].__class__ == BlueSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, BLUE_SQUARE_TEXTURE))
            elif elem[2].__class__ == GraySquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, GRAY_SQUARE_TEXTURE))
            elif elem[2].__class__ == StartSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, START_SQUARE_TEXTURE))
            elif elem[2].__class__ == RetrySquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, RETRY_SQUARE_TEXTURE))
            elif elem[2].__class__ == GameOverSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, GAMEOVER_SQUARE_TEXTURE))

    def remove_all_squares(self, sprite_group):
        for sprite in self.squares_to_draw:
            sprite_group.remove(sprite)
            # sprite.kill()


class Grid:
    def __init__(self, game):
        self.size = (5, 5)
        self.grid = list()
        self.game = game
        self.generate_zero_grid()

    def generate_zero_grid(self):
        self.grid = []
        for i in range(5):
            self.grid.append([0] * 5)

    def generate_new_pattern(self):
        import random
        for i in range(3):
            while True:
                x = random.randint(0, self.size[0] - 1)
                y = random.randint(0, self.size[1] - 1)
                if self.grid[y][x] == 0:
                    coords = x, y
                    self.grid[y][x] = GraySquare(self.game, GRAY_SQUARE_TEXTURE, coords)
                    break

    def replace_gray_by_random(self):
        import random
        max_r = 7
        # 1 - 5 green, 6 red, 7 blue, 8 - 9 orange
        a = [random.randint(0, max_r), random.randint(0, max_r), random.randint(0, max_r)]
        if a == [6, 6, 6]:
            a = [6, 7, 1]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] != 0:
                    if self.grid[i][j].__class__ == GraySquare:
                        index = a.pop()
                        coords = i, j
                        if index <= 5:
                            self.grid[i][j] = GreenSquare(self.game, GREEN_SQUARE_TEXTURE, coords)
                        elif index == 6:
                            self.grid[i][j] = RedSquare(self.game, RED_SQUARE_TEXTURE, coords)
                        elif index == 7:
                            self.grid[i][j] = BlueSquare(self.game, BLUE_SQUARE_TEXTURE, coords)

    def destroy_reds(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] != 0:
                    if self.grid[i][j].__class__ == RedSquare:
                        self.grid[i][j] = 0

    def try_to_generate(self):
        if self.grid == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]:
            self.generate_new_pattern()
            self.replace_gray_by_random()
            self.generate_new_pattern()
            return "new game generated"
        leftovers = []
        for line in self.grid:
            for x in line:
                if x != 0:
                    leftovers.append(x.__class__.__name__)
        if set(leftovers) == {"RedSquare", "GraySquare"} or set(leftovers) == {"GraySquare"}:
            self.destroy_reds()
            self.replace_gray_by_random()
            self.generate_new_pattern()

    def click_cell(self, cell):
        if cell == "no cell":
            if self.game.state == "running":
                self.game.combo = 0
                self.game.time -= self.game.time_multiplier
                play_sound("missclick.mp3")
        else:
            cell[1] = self.size[1] - cell[1] - 1
            if self.grid[cell[1]][cell[0]] != 0:
                self.grid[cell[1]][cell[0]].on_click()
                print(self.grid[cell[1]][cell[1]])
            else:
                self.click_cell("no cell")

    def get_squares(self):
        squares = list()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] != 0:
                    squares.append([i, j, self.grid[i][j]])
        return squares

    def remove_square(self, coords):
        return

    def test(self, coords):
        if self.grid[coords[1]][coords[0]] != 0 and self.grid[coords[1]][coords[0]].__class__ not in [GraySquare, GameOverSquare]:
            self.grid[coords[1]][coords[0]] = 0

    def init_start_button(self):
        coords = [2, 1]
        self.grid[2][1] = StartSquare(self.game, START_SQUARE_TEXTURE, coords)
        self.grid[2][2] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        self.grid[2][3] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)

    def init_retry_screen(self):
        self.generate_zero_grid()
        coords = [3, 1]
        self.grid[3][1] = RetrySquare(self.game, RETRY_SQUARE_TEXTURE, coords)
        self.grid[3][2] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        self.grid[3][3] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        coords = [1, 0]
        self.grid[1][0] = GameOverSquare(self.game, GAMEOVER_SQUARE_TEXTURE, coords)