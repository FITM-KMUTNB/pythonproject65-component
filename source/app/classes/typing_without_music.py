from .. import engine, program
from . import pages

from pygame.locals import *
from pygame_gui.core import ObjectID

import webbrowser
import pygame_gui
import pygame
import random
import math
import time
import sys
import os

class TypingWithoutMusic(engine.Engine):
    
    
    def __init__(self, display_title: str, rect: Rect, theme: str = None, scrolling_background: bool = False):
        pygame.display.set_caption(display_title)
        
        self.display_title = display_title
        
        self.theme = theme
        
        self.scrolling_background: bool = scrolling_background
        
        self.rect = rect
        self.width: int = rect.size[0]
        self.height: int = rect.size[1]
        
        self.music_mixer_channel = pygame.mixer.Channel(1)
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/background.jpg').convert()
        
        self.sunshine_typing_logo = pygame.image.load(os.getcwd() + '/source/app/assets/image/sunshine_typing_logo.png').convert()
        
        self.scroll: int = 0
        self.tiles: int = math.ceil(self.width / self.background_image.get_width()) + 1
        
        self.ui_manager = pygame_gui.UIManager(rect.size, theme)
    
        self.ui_menu = pages
        
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
        
    
    def run(self) -> None:
        clock = pygame.time.Clock()
        is_running: bool = True
        
        sunshine_typing_logo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 240, 80),
                (500, 300)
            ),
            image_surface=self.sunshine_typing_logo,
            manager=self.ui_manager
        )
        
        play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@play_button')
        )
        
        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 320, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@exit_button')
        )
        
        scoreboard_sign_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width - 170, -10),
                (150, 150)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@scoreboard_sign_button')
        )
        
        music_opened_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width - 330, -15),
                (150, 150)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@music_closed_button'),
        )
        
        enabled_audio = program.Typing(
            self.display_title,
            self.rect,
            self.theme,
        )
        
        scoreboard_page = pages.Scoreboard(
            rect=self.rect, 
            theme=self.theme, 
            music=False,
        )
        
        play_game_state: bool = False 
        enabled_audio_state: bool = False
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
                            
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == play_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                           
                        play_game_state = True
                        
                    if event.ui_element == music_opened_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        enabled_audio_state = True
                        
                    if event.ui_element == scoreboard_sign_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()   
                        
                        scoreboard_page.initialize()
                    
                    if event.ui_element == exit_button:             
                        pygame.quit()
                        exit()
                    
                self.ui_manager.process_events(event)
                    
            self.ui_manager.update(time_delta)
            self.scroll_background(enabled=self.scrolling_background)
            
            if play_game_state and not enabled_audio_state:
                self.ui_menu.Play(
                    rect=self.rect,
                    theme=self.theme,
                    music=False,
                    scrolling_background=self.scrolling_background
                ).initialize()
            
            if enabled_audio_state:
                self.music_mixer_channel.unpause()
                enabled_audio.run()
            
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()
