from app.configurations import configure
from app import program
from pygame.locals import *

import os


configure.WINDOW_NAME = 'Sunshine Typing By Component Team'
configure.WINDOW_RECT = Rect(0, 0, 1280, 720)
configure.GAME_THEME_PATH = os.getcwd() + '/source/app/data/themes/default_theme.json'
configure.SENTENCES_PATH = os.getcwd() + '/sentences.txt'
configure.ENABLED_SCROLLING_BACKGROUND = False


if __name__ == '__main__':
    bootstrap = program.Typing(
        display_title=configure.WINDOW_NAME,
        rect=configure.WINDOW_RECT,
        theme=configure.GAME_THEME_PATH,
        scrolling_background=configure.ENABLED_SCROLLING_BACKGROUND
    ).run()