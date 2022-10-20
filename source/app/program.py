from . import engine
from .classes import ui_element
from pygame.locals import *

import pygame_gui
import pygame
import random
import time
import sys

class Typing(engine.Engine):
    """
    About typing test game using pygame to create game which is a project at King Mongkut's University of Technology North Bangkok. 
    By students of information of network engineering, there are 6 project groups, you can see it in our config file.
    
    Instructions:
    You must include a variable which is a Class constructor,
    which contains display_title, width, and height, to be used as part of the program.
    
    Example as a Code:
    from pygame.locals import *
    
    rect: Rect = Rect(0, 0, 1280, 720)
    
    typing_game: Typing = Typing('untitled', rect)
    typing_game.run()
    """
    
    
    def __init__(self, display_title: str, rect: Rect, theme: str = None):
        pygame.display.set_caption(display_title)
        
        theme = theme if theme is not None else theme
        
        self.width: int = rect.size[0]
        self.height: int = rect.size[1]
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background.fill(pygame.Color('#242424'))
        
        self.ui_manager = pygame_gui.UIManager(rect.size)
        self.ui_manager.get_theme().load_theme(theme)
        
        self.ui_menu = ui_element.Menu(
            width=self.width,
            height=self.height,
            manager=self.ui_manager
        )
        
    
    def run(self) -> None:
        clock = pygame.time.Clock()
        self.is_running: bool = True
        
        self.ui_menu.initialize()
        
        while self.is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == exit_button:
                        pygame.quit()
                        exit()
                    
                self.ui_manager.process_events(event)
                    
            self.ui_manager.update(time_delta)
                    
            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()
