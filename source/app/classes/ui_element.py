from pygame_gui.core.interfaces import IUIManagerInterface

import pygame_gui
import pygame

   
class Menu:
    def __init__(self, width: int, height: int, manager: IUIManagerInterface):
        self.width = width
        self.height = height
        self.ui_manager = manager
        
    def initialize(self):
        welcome_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 50, 150),
                (100, 50)
            ),
            text='Typing Test',
            manager=self.ui_manager
        )
        
        play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 100, 250),
                (200, 100)
            ),
            text='Play',
            manager=self.ui_manager
        )
        
        scoreboard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 100, 350),
                (200, 100)
            ),
            text='Scoreboard',
            manager=self.ui_manager
        )
        
        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 100, 450),
                (200, 100)
            ),
            text='Exit',
            manager=self.ui_manager
        )