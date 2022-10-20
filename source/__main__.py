import os

from app import program
from pygame.locals import *

WINDOW_RECT: Rect = Rect(0, 0, 1280, 720)

if __name__ == '__main__':
    bootstrap = program.Typing(
        display_title='Typing Test',
        rect=WINDOW_RECT,
        theme=os.getcwd() + '/theme.json'
    )
    bootstrap.run()