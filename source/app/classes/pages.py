from .. import program
from . import typing_without_music
from ..configurations import configure

from pygame.locals import *
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface

import pygame_gui
import pygame
import os


class Play:
    def __init__(self, window_width: int, window_height: int, theme: str, enabled_music: bool):
        self.width = window_width
        self.height = window_height
        
        self.enabled_music = enabled_music
        
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color('#444444'))
        
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.ui_manager.get_theme().load_theme(theme)
        
        self.username: str = ''
        
        
    def initialize(self): 
        clock = pygame.time.Clock()
        is_running: bool = True
        
        name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 240, 80),
                (500, 300)
            ),
            manager=self.ui_manager,
        )
        
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@back_button')
        )
        
        typing_with_music_menu = program.Typing(
            display_title=configure.WINDOW_NAME,
            rect=configure.WINDOW_RECT,
            theme=configure.GAME_THEME_PATH,
            scrolling_background=configure.ENABLED_SCROLLING_BACKGROUND
        )
        
        typing_without_music_menu = typing_without_music.TypingWithoutMusic(
            display_title=configure.WINDOW_NAME,
            rect=configure.WINDOW_RECT,
            theme=configure.GAME_THEME_PATH,
            scrolling_background=configure.ENABLED_SCROLLING_BACKGROUND
        )
        
        back_previous_page_state: bool = False
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_TEXT_ENTRY_CHANGED):
                    print("Changed text:", event.text)
                    
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == back_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        back_previous_page_state = True
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            
            self.window_surface.blit(self.background, (0, 0))
        
            if back_previous_page_state and self.enabled_music:
                print("PLAY ENABLED MUSIC")
                typing_with_music_menu.run()
                
            if back_previous_page_state and not self.enabled_music:
                print("PLAY DISABLED MUSIC")
                typing_without_music_menu.run()
            
            self.ui_manager.draw_ui(self.window_surface)
                    
            pygame.display.update()
    
    
class Scoreboard:
    def __init__(self, window_width: int, window_height: int, theme: str):
        self.width = window_width
        self.height = window_height
        
        self.window_surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color('#444444'))
        
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.ui_manager.get_theme().load_theme(theme)
        
        
    def initialize(self):
        clock = pygame.time.Clock()
        is_running: bool = True
        
        test_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 50, 150),
                (100, 50)
            ),
            text='ELEMENT WANNA CLASS',
            manager=self.ui_manager
        )
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            
            self.window_surface.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)
                    
            pygame.display.update()
            