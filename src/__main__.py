import os
import pygame
import pygame_gui

from pygame_gui.core import ObjectID
from pygame.locals import *
from pygame import mixer
from sys import exit

WIDTH: int = 1624
HEIGHT: int = 1080

MyFont = pygame.font.SysFont("8-bit_Arcade_In.ttf",15)

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Component App')

        mixer.init()
        mixer.music.load(os.getcwd() + '/music/root_music.mp3')
        mixer.music.play(loops=1)
        mixer.music.set_volume(0.3)

        self.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.rect.size)
        self.background = pygame.image.load(os.getcwd() + '/images/root_background.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.manager.get_theme().load_theme('./__provider__.json')

        window_root_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect((0, 0), (WIDTH, HEIGHT)),
            is_window_root_container=True,
            manager=self.manager
        )

        player_container_rect = pygame.Rect((0, 0), (WIDTH / 2, 1080))
        player_container = pygame_gui.core.UIContainer(
            relative_rect=player_container_rect,
            container=window_root_container,
            manager=self.manager
        )

        player_configuration_rect = pygame.Rect((1000, 0), (650, 1080))
        player_configuration_container = pygame_gui.core.UIContainer(
            relative_rect=player_configuration_rect,
            container=window_root_container,
            manager=self.manager
        )
#settng botton
        hello_button_rect = pygame.Rect((520, 5), (100, 50))
        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=hello_button_rect,
            text='Settings',
            container=player_configuration_container,
            manager=self.manager
        )
#play botton
        play_button_rect = pygame.Rect((0, 0), (300, 100))
        play_button_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=play_button_rect,
            text=MyFont.render("Play",True,("Blue")),
            container=window_root_container,
            manager=self.manager
        )

        self.clock = pygame.time.Clock()
        self.running: bool = True

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()

                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == self.hello_button:
                        print('Hello, World!')

                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))
            self.manager.draw_ui(self.screen)

            pygame.display.update()
            

if __name__ == '__main__':
    App().run()
