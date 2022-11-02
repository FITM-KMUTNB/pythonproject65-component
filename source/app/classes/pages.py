from ..configurations import configure
from . import typing_without_music
from ..contexts import store
from ..core import game
from .. import program

from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.core import ObjectID
from pygame.locals import *

import pygame_gui
import sqlite3
import pygame
import os


database = sqlite3.connect("sunshine_typing.db")
database_cursor = database.cursor()


class Play:
    
    
    def __init__(self, rect: Rect, theme: str, music: bool, scrolling_background: bool = False):
        self.rect = rect
        self.width = rect.size[0]
        self.height = rect.size[1]
        
        self.theme = theme
        
        self.music = music
        
        self.scrolling_background = scrolling_background
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/prepare_background.png').convert()
        
        self.mini_sunshine_typing_logo = pygame.image.load(os.getcwd() + '/source/app/assets/image/mini_sunshine_typing_logo.png')
        self.entry_name_background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/entry_name_background.png')
        self.name_label = pygame.image.load(os.getcwd() + '/source/app/assets/image/name_label.png')
        
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
            
    
    def username_verify(self, payload: str):
        if len(payload) > 1:
            return True
        
        return False
        
        
    def initialize(self): 
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
        
        entry_name_background = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 340, 375),
                (265, 265)
            ),
            image_surface=self.entry_name_background_image,
            manager=self.ui_manager,
        )
        
        name_label = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 340, 365),
                (200, 100)
            ),
            image_surface=self.name_label,
            manager=self.ui_manager,
        )
        
        username_condition_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 270, 650),
                (650, 60)
            ),
            text='Name must be more than two characters',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@username_condition_label')
        )
        
        name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 373, 475),
                (200, 75)
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@entry_name')
        )
        
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 320, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@start_button')
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
        
        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@back_button')
        )
        
        start_game = game.Game(
            rect=self.rect,
            theme=self.theme,
            music=self.music
        )
        
        scoreboard_page = Scoreboard(
            rect=self.rect, 
            theme=self.theme, 
            music=True,
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
        
        start_game_state: bool = False
        username_state: bool = False
        back_previous_page_state: bool = False
        
        set_username: str = ""
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_TEXT_ENTRY_CHANGED):                        
                    username_state = self.username_verify(event.text)
                    
                    if username_state:
                        set_username = event.text
                    
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == start_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        if username_state:
                            store.username = set_username
                            start_game_state = True
                        
                    if event.ui_element == back_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        back_previous_page_state = True
                        
                    if event.ui_element == scoreboard_sign_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        scoreboard_page.initialize()
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            
            self.scroll_background(enabled=self.scrolling_background)
            
            if start_game_state:
                start_game.start()
        
            if back_previous_page_state and self.music:
                typing_with_music_menu.run()
                
            if back_previous_page_state and not self.music:
                typing_without_music_menu.run()
            
            self.ui_manager.draw_ui(self.window_surface)
                    
            pygame.display.update()
            

class Scoreboard:
    
    
    def __init__(self, rect: Rect, theme: str, music: bool, scrolling_background: bool = False):
        self.rect = rect
        self.width = rect.size[0]
        self.height = rect.size[1]
        
        self.theme = theme
        
        self.music = music
        
        self.scrolling_background = scrolling_background
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/prepare_background.png').convert()
        
        self.mini_sunshine_typing_logo = pygame.image.load(os.getcwd() + '/source/app/assets/image/mini_sunshine_typing_logo.png')
        
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
        

    def initialize(self) -> None:
        clock = pygame.time.Clock()
        is_running: bool = True
        
        fetch_desc_rows = database_cursor.execute(
            "SELECT username, wpm FROM typing ORDER BY wpm DESC LIMIT 5;"
        ).fetchall()
        database.commit()
        
        mini_sunshine_typing_logo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (-50, 10),
                (350, 150)
            ),
            image_surface=self.mini_sunshine_typing_logo,
            manager=self.ui_manager,
        )
        
        top_rankings_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 30),
                (650, 100)
            ),
            text='Top 5 from lastest game',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@top_rankings_title')
        )
        
        first_ranking = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 150),
                (650, 100)
            ),
            text="{} {}".format(
                fetch_desc_rows[0][0],
                int(fetch_desc_rows[0][1])
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@top_ranking")
        )
        
        second_ranking = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 200),
                (650, 100)
            ),
            text="{} {}".format(
                fetch_desc_rows[1][0],
                int(fetch_desc_rows[1][1])
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@top_ranking")
        )   
        
        third_ranking = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 250),
                (650, 100)
            ),
            text="{} {}".format(
                fetch_desc_rows[2][0],
                int(fetch_desc_rows[2][1])
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@top_ranking")
        )   
        
        fourth_ranking = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 300),
                (650, 100)
            ),
            text="{} {}".format(
                fetch_desc_rows[3][0],
                int(fetch_desc_rows[3][1])
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@top_ranking")
        )   
        
        five_ranking = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 320, 350),
                (650, 100)
            ),
            text="{} {}".format(
                fetch_desc_rows[4][0],
                int(fetch_desc_rows[4][1])
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@top_ranking")
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
        
        back_previous_page_state = False
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == back_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        back_previous_page_state = True
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            
            self.scroll_background(enabled=self.scrolling_background)
                
            if back_previous_page_state and self.music:
                typing_with_music_menu.run()
                
            if back_previous_page_state and not self.music:
                typing_without_music_menu.run()
                
            self.ui_manager.draw_ui(self.window_surface)
                    
            pygame.display.update()
    