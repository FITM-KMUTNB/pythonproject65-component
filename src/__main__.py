import os
import pygame

from typing import Any, Dict, List, Optional, SupportsInt, Tuple, Union
from pygame.locals import *
from pygame import mixer
from sys import exit

WIDTH: int = 1624
HEIGHT: int = 1080

EventType = Union[SupportsInt, Tuple[SupportsInt, ...], List[SupportsInt]]

class Button:
    def __init__(self, text: str, position: set, font_family: str, font_size: int, background: str, feedback: str):
        self.x, self.y = position
        self.font = pygame.font.SysFont(font_family, font_size)
        
        if feedback.__eq__(''):
            self.feedback = 'default text'
        else:
            self.feedback = feedback

    def on_click(self, event: Optional[EventType] = None):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Component App')

        mixer.init()
        mixer.music.load('./src/music/root_music.mp3')
        mixer.music.play(loops=1)
        mixer.music.set_volume(0.3)

        self.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.rect.size)
        self.background = pygame.image.load('./src/images/root_background.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.running: bool = True

    def run(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()

                pygame.display.update()

if __name__ == '__main__':
    App().run()
