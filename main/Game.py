
import os
import core
import pygame
from modules import *


def main(core):

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((core.WIDTH, core.HEIGHT))
    pygame.display.set_caption(core.TITLE)

    sounds = {}
    for key, value in core.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
        sounds[key].set_volume(1)

    is_dual_mode = gameStartInterface(screen, core)

    levelfilepaths = [os.path.join(core.LEVELFILEDIR, filename) for filename in sorted(os.listdir(core.LEVELFILEDIR))]

    for idx, levelfilepath in enumerate(levelfilepaths):
        switchLevelIterface(screen, core, idx+1)
        game_level = GameLevel(idx+1, levelfilepath, sounds, is_dual_mode, core)
        is_win = game_level.start(screen)
        if not is_win: break
    is_quit_game = gameEndIterface(screen, core, is_win)
    return is_quit_game


if __name__ == '__main__':
    while True:
        is_quit_game = main(core)
        if is_quit_game:
            break