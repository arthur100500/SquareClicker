import pygame
import pygame_gui
import os
import requests

print(30111 % 92)
# globals
direction = 0
note = 1
user = ['', '', False]
server_ip = '213.187.116.225'
server_port = '10000'
file = 'memory.txt'
volume = 1.0


def write_to_file(change):
    # format: "row: value"
    text = 'error'
    with open(file, 'r') as f:
        text = list(f)
        for i in range(len(text)):
            if text[i].split(': ')[0] == change.split(': ')[0]:
                text[i] = change + '\n'
    if change.split(': ')[0] not in text:
        text.append(change + '\n')
    with open(file, 'w') as f:
        f.write(''.join(text))


def read_from_file(row):
    try:
        with open(file) as f:
            text = list(f)
            for i in text:
                if i.split(': ')[0] == row:
                    return ''.join(i.split(': ')[1::]).replace('\n', '')
    except FileNotFoundError:
        open(file, 'w').close()


def send_highscore(score):
    score = int(score)
    print(score, user[0])
    secret_key = int((score ** 5 * len(user[0] + "12223" * len(str(len(user[0])))) + score ** 2) % 1234567890 + len(
        user[0] + "123" * len(user[0])) % 2000001 + score ** 40 % 1234567890)
    print(secret_key)
    requests.get('http://' + server_ip + ':' + server_port + '/set_rec/' + str(score) + '/' + user[0] + '/' + user[
        1] + '/' + str(secret_key))


def check_user(data):
    r = requests.get('http://' + server_ip + ':' + server_port + '/check_user_data/' + data[0] + '/' + data[1] + '')
    if r.status_code == 200:
        if r.text not in ['incorrect password', 'invalid username']:
            data[2] = True
        return r.text
    return 'invalid username'


def launch_settings_screen():
    global screen
    global user
    global volume
    not_exited = True
    manager = pygame_gui.UIManager((800, 600))
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 259), (548, 50)), text='Громкость звуков',
                                manager=manager)
    volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 330), (548, 30)),
                                                           manager=manager, start_value=volume * 100,
                                                           value_range=[1, 100])
    info = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 20), (548, 50)),
                                       text='Авторизируйтесь, используя почту и пароль', manager=manager)
    textbox1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 80), (300, 50)), manager=manager)
    textbox2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((20, 120), (300, 50)), manager=manager)
    if len(user) == 3 and user[2]:
        info.set_text('Здравствуй, ' + check_user(user))
        textbox1.set_text(user[0])
        textbox2.set_text(user[1])
    button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((329, 90), (100, 50)),
                                           text='Log In',
                                           manager=manager)
    pygame.display.set_caption('SquareClicker - Options')
    clock = pygame.time.Clock()
    while not_exited:
        time_delta = clock.tick(60) / 1000.0
        screen.fill(fill_color)
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                not_exited = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    not_exited = False
            if event.type == pygame.MOUSEBUTTONUP:
                volume = volume_slider.current_value / 100
                pygame.mixer.music.set_volume(volume ** 2)
                write_to_file('volume: ' + str(volume))
                print(volume)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button1:
                        user = [textbox1.text, textbox2.text, False]
                        a = check_user(user)
                        if a == 'invalid username':
                            info.set_text('Неправильная почта')
                        elif a == 'incorrect password':
                            info.set_text('Неправильный пароль')
                        else:
                            print(121)
                            write_to_file('user: ' + user[0])
                            write_to_file('pwd: ' + user[1])
                            info.set_text('Здравствуй, ' + a)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.display.set_caption('SquareClicker')
    return


def init_sound_system():
    pygame.mixer.pre_init(44100, -16, 2, 1024)  # setup mixer to avoid sound lag
    pygame.init()
    pygame.mixer.init()


def play_sound(sound):
    pygame.mixer.music.load(SKIN_PATH + "\\" + sound)
    pygame.mixer.music.play()


class Square:
    def __init__(self, game, texture_path, coords):
        self.size = 16 * 6
        self.type = ""
        self.game = game
        self.texture = texture_path
        self.coords = coords

    def on_click(self):
        pass

    def draw(self):
        pass


class GreenSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.time += self.game.time_multiplier / 30
        self.game.combo += 1
        self.game.score += self.game.combo ** 0.5
        self.game.grid.remove_square(self.coords)
        play_sound("note.mp3")

    def __str__(self):
        return "g"


class RedSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.combo = 0
        self.game.time -= 4 * self.game.time_multiplier
        self.game.grid.remove_square(self.coords)
        play_sound("redsound.mp3")

    def __str__(self):
        return "r"


class BlueSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.combo += 1
        self.game.time += self.game.time_multiplier
        self.game.score += self.game.combo ** 0.8 * 5
        self.game.grid.remove_square(self.coords)
        play_sound('bluesound.mp3')

    def __str__(self):
        return "b"


class OrangeSquare(Square):
    def __init__(self, game, texture_path, coords, numb):
        self.numb = numb
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.combo += 1
        self.game.score += self.game.combo ** 0.8 * 5
        if self.numb > 1:
            self.game.time += self.game.time_multiplier / 30
            self.game.grid.grid[self.coords[0]][self.coords[1]] = OrangeSquare(self.game, "", self.coords,
                                                                               self.numb - 1)
        else:
            self.game.time += self.game.time_multiplier / 3
            self.game.grid.grid[self.coords[0]][self.coords[1]] = 0
        self.game.grid.remove_square(self.coords)
        global note
        global direction
        play_sound('orange' + str(self.numb) + '.mp3')

    def __str__(self):
        return "o"


class GraySquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        pass

    def __str__(self):
        return "G"


class BackgroundSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.start()

    def __str__(self):
        return "B"


class StartSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.start()

    def __str__(self):
        return "START"


class CogSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        launch_settings_screen()

    def __str__(self):
        return "c"


class RetrySquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.start()

    def __str__(self):
        return "RETRY"


class GameOverSquare(Square):
    def __init__(self, game, texture_path, coords):
        super().__init__(game, texture_path, coords)

    def on_click(self):
        pass

    def __str__(self):
        return "GAMEOVER"


def load_image(name, colorkey=None):
    global SKIN_PATH
    fullname = os.path.join(SKIN_PATH, name)
    image = pygame.image.load(fullname).convert_alpha()
    if colorkey == 2:
        image = pygame.image.load(fullname).convert()
    return image


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, group, pos, texture):
        super().__init__(group)
        image = load_image(texture, colorkey=-1)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])


# constants
COGSQUARE_TEXTURE = "cogsquare6x.png"
BACKGROUND_TEXTURE = "playfield26x.png"
GRAY_SQUARE_TEXTURE = "graysquare6x.png"
GREEN_SQUARE_TEXTURE = "greensquare6x.png"
RED_SQUARE_TEXTURE = "redsquare6x.png"
BLUE_SQUARE_TEXTURE = "bluesquare6x.png"
START_SQUARE_TEXTURE = "start6x.png"
BG_SQUARE_TEXTURE = "transparentpixel.png"
RETRY_SQUARE_TEXTURE = "retry6x.png"
GAMEOVER_SQUARE_TEXTURE = "gameover6x.png"
ORANGESQUARE1_TEXTURE = "orangesquare16x.png"
ORANGESQUARE2_TEXTURE = "orangesquare26x.png"
ORANGESQUARE3_TEXTURE = "orangesquare36x.png"


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
        self.max_combo = 0
        self.time_multiplier = 3.5
        self.grid_size = 19 * 6
        self.window_size = size
        self.squares_to_draw = []
        self.sprite_group = sprite_group
        self.change_state = True
        self.health_points = 1

    def on_click(self, x, y):
        self.max_combo = max(self.max_combo, self.combo)
        cell = self.detect_cell(x, y)
        if cell:
            self.grid.click_cell(cell)
            if cell != "no cell":
                self.grid.test(cell)

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
        self.max_combo = 0
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
            self.time = min(self.time, self.initial_time)
        self.last_tick_time = time()
        self.health_points = self.time / self.initial_time
        # if lost
        if self.time < 0:
            # defeat
            time = 10
            if len(user) == 3 and user[2]:
                send_highscore(self.score)
            play_sound("zvukiprajeniya.mp3")
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
            pygame.draw.rect(screen, (
                int(255 * (abs(x - 1) - abs(x - 0.5) + 0.5)), int(255 * (1 - (abs(x - 0.5) - abs(x) + 0.5))), 0),
                             (0, self.window_size[1] - 600, int(self.health_points * 588), 12))

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
            elif elem[2].__class__ == OrangeSquare:
                if elem[2].numb == 3:
                    self.squares_to_draw.append(BaseSprite(sprite_group, coords, ORANGESQUARE3_TEXTURE))
                if elem[2].numb == 2:
                    self.squares_to_draw.append(BaseSprite(sprite_group, coords, ORANGESQUARE2_TEXTURE))
                if elem[2].numb == 1:
                    self.squares_to_draw.append(BaseSprite(sprite_group, coords, ORANGESQUARE1_TEXTURE))
            elif elem[2].__class__ == CogSquare:
                self.squares_to_draw.append(BaseSprite(sprite_group, coords, COGSQUARE_TEXTURE))

    def remove_all_squares(self, sprite_group):
        for sprite in self.squares_to_draw:
            sprite_group.remove(sprite)
            sprite.kill()
        self.squares_to_draw.clear()


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
        max_r = 8
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
                            if self.game.time < self.game.initial_time / 3 and index % 2 == 0:
                                self.grid[i][j] = BlueSquare(self.game, GREEN_SQUARE_TEXTURE, coords)
                            else:
                                self.grid[i][j] = GreenSquare(self.game, GREEN_SQUARE_TEXTURE, coords)
                        elif index == 6:
                            self.grid[i][j] = RedSquare(self.game, RED_SQUARE_TEXTURE, coords)
                        elif index == 7:
                            self.grid[i][j] = BlueSquare(self.game, BLUE_SQUARE_TEXTURE, coords)
                        elif index == 8:
                            self.grid[i][j] = OrangeSquare(self.game, ORANGESQUARE1_TEXTURE, coords, 3)

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

    def test(self, coords, destroy_orange=False):
        if self.grid[coords[1]][coords[0]] != 0 and self.grid[coords[1]][coords[0]].__class__ not in [GraySquare,
                                                                                                      GameOverSquare,
                                                                                                      OrangeSquare,
                                                                                                      CogSquare]:
            self.grid[coords[1]][coords[0]] = 0

    def init_start_button(self):
        coords = [2, 1]
        self.grid[4][4] = CogSquare(self.game, COGSQUARE_TEXTURE, [4, 4])
        self.grid[2][1] = StartSquare(self.game, START_SQUARE_TEXTURE, coords)
        self.grid[2][2] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        self.grid[2][3] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)

    def init_retry_screen(self):
        self.generate_zero_grid()
        coords = [2, 1]
        self.grid[4][4] = CogSquare(self.game, COGSQUARE_TEXTURE, [4, 4])
        self.grid[2][1] = RetrySquare(self.game, RETRY_SQUARE_TEXTURE, coords)
        self.grid[2][2] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        self.grid[2][3] = BackgroundSquare(self.game, BG_SQUARE_TEXTURE, coords)
        coords = [1, 0]
        self.grid[1][0] = GameOverSquare(self.game, GAMEOVER_SQUARE_TEXTURE, coords)


running = True
size = width, height = 588, 666
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
game = Game(size, all_sprites, self_playing=False)
SKIN_PATH = 'textures'
pygame.font.init()
font = 'bahnschrift'
font1 = pygame.font.SysFont(font, 72)
background = BaseSprite(all_sprites, (0, height - 588), BACKGROUND_TEXTURE)
game.begin()
init_sound_system()
game.draw_health(screen)
fill_color = (70, 70, 70)
pygame.display.set_caption('SquareClicker')

user[0] = read_from_file('user')
user[1] = read_from_file('pwd')
if read_from_file('volume') is not None:
    volume = float(read_from_file('volume'))
    pygame.mixer.music.set_volume(volume ** 2)
if user[0] is not None and user[1] is not None:
    check_user(user)

while running:
    screen.fill(fill_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            game.on_click(*pygame.mouse.get_pos())
    game.tick()
    all_sprites.draw(screen)
    game.draw_health(screen)
    img1 = font1.render(str(int(game.score)), True, (255, 255, 255))
    if game.state == 'over':
        img2 = font1.render('x' + str(int(game.max_combo)), True, (255, 255, 255))
    if game.state == 'running':
        img2 = font1.render('x' + str(int(game.combo)), True, (255, 255, 255))
    if game.state == 'not started':
        img2 = font1.render('', True, (255, 255, 255))
    screen.blit(img1, (0, -10))
    screen.blit(img2, (size[0] - 70 - 26 * len(str(game.combo)), -10))
    pygame.display.flip()
    game.remove_all_squares(all_sprites)

pygame.quit()
