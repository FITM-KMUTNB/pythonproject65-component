from ..configurations import configure
from .. import engine

from pygame.locals import *

import pygame_gui
import pygame
import random
import time
import sys
import os

class Game(engine.Engine):
    
    
    def __init__(self, rect: Rect, theme: str):
        self.rect = rect
        self.width = rect.size[0]
        self.height = rect.size[1]
        
        self.theme = theme
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/core_background.png').convert()
        
        self.mini_sunshine_typing_logo = pygame.image.load(os.getcwd() + '/source/app/assets/image/mini_sunshine_typing_logo.png').convert()
        
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.ui_manager.get_theme().load_theme(theme)
        
        
    def scroll_background(self, enabled: bool = False):
        if enabled:
            counter: int = 0
            while counter < self.tiles:
                self.window_surface.blit(
                    self.background_image,
                    (self.background_image.get_width() * counter + self.scroll, 0)
                )
                counter += 1
                
            self.scroll -= 6
            
            if abs(scroll) > self.background_image.get_width():
                scroll = 0
                
        else:
            self.window_surface.blit(self.background_image, (0, 0))
        
                
    def random_sentence(self, filename: str):
        file = open(filename).read()
        sentences = file.split('\n')
        receive_sentence = random.choice(sentences)
        
        return sentences
    
    
    def start(self) -> None:
        clock = pygame.time.Clock()
        is_running: bool = True
        
        mini_sunshine_typing_logo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (-50, 10),
                (350, 150)
            ),
            image_surface=self.mini_sunshine_typing_logo,
            manager=self.ui_manager,
        )
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            self.scroll_background(enabled=configure.ENABLED_SCROLLING_BACKGROUND)
            
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()