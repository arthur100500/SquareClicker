import pygame
import os
SKIN_PATH = "data"

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
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])