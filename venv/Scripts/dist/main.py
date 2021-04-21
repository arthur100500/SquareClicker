from game import *
import square
import misc
import pygame
import random
# variables
running = True
size = width, height = 588, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
game = Game(size, all_sprites, self_playing=False)


# set skin
misc.SKIN_PATH = 'textures'

# text
pygame.font.init()
font = random.choice(pygame.font.get_fonts())
font1 = pygame.font.SysFont(font, 72)
print(font)

# game sprites
background = BaseSprite(all_sprites, (0, height - 588), BACKGROUND_TEXTURE)

# start everything
game.begin()
square.init_sound_system()
game.draw_health(screen)

# main the loop a
while running:
    screen.fill((117, 117, 117))
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            game.on_click(*pygame.mouse.get_pos())
    # game
    game.tick()
    # game.print_grid()
    # draw
    all_sprites.draw(screen)
    game.draw_health(screen)
    img1 = font1.render(str(int(game.score)), True, (255, 255, 255))
    screen.blit(img1, (0, 0))
    pygame.display.flip()
    # clear_draw
    game.remove_all_squares(all_sprites)

pygame.quit()