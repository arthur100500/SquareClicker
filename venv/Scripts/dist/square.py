import pygame
import misc

# globals
direction = 0
note = 1


def init_sound_system():
    pygame.mixer.pre_init(44100, -16, 2, 1024)  # setup mixer to avoid sound lag
    pygame.init()
    pygame.mixer.init()


def play_sound(sound):
    pygame.mixer.music.load(misc.SKIN_PATH + "\\" + sound)
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
        self.game.combo += 1
        self.game.score += self.game.combo ** 0.5
        self.game.grid.remove_square(self.coords)
        global direction
        global note
        play_sound("note" + str(note) + ".mp3")
        if direction == 0:
            note += 1
        elif direction == 1:
            note -= 1
        if note == 5:
            direction = 1
        if note == 1:
            direction = 0

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
        global direction
        global note
        play_sound("note" + str(note) + ".mp3")
        if direction == 0:
            note += 1
        elif direction == 1:
            note -= 1
        if note == 5:
            direction = 1
        if note == 1:
            direction = 0

    def __str__(self):
        return "b"


class OrangeSquare(Square):
    def __init__(self, game, texture_path, coords):
        self.numb = 3
        super().__init__(game, texture_path, coords)

    def on_click(self):
        super().on_click()
        self.game.combo += 1
        self.game.score += self.game.combo ** 0.8 * 5
        self.game.grid.remove_square(self.coords)
        # + spawning another circle -1 in prev. point

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
