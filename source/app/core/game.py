from ..classes import typing_without_music, pages
from ..configurations import configure
from ..contexts import store
from .. import program
from .. import engine

from pygame_gui.core import ObjectID
from pygame.locals import *

import pygame_gui
import sqlite3
import pygame
import random
import time
import sys
import os


database = sqlite3.connect("sunshine_typing.db")
database_cursor = database.cursor()

class Game(engine.Engine):
    
    
    def __init__(self, rect: Rect, theme: str, music: bool):
        self.rect = rect
        self.width = rect.size[0]
        self.height = rect.size[1]
        
        self.theme = theme
        
        self.music = music
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/core_background.png').convert()
        
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
        
                
    def random_sentence(self) -> str:
        file = open(os.getcwd() + "/sentences.txt").read()
        sentences = file.split('\n')
        receive_sentence = random.choice(sentences)
        
        return sentences
    
    def start(self) -> None:
        clock = pygame.time.Clock()
        is_running: bool = True
        
        random_challenge: str = self.random_sentence()
        sentence_challenge = random_challenge[random.randint(0, 2)]
        
        counter: int = 0
        sentence: str = ""
        
        mini_sunshine_typing_logo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                (-50, 10),
                (350, 150)
            ),
            image_surface=self.mini_sunshine_typing_logo,
            manager=self.ui_manager,
        )
        
        sentence_label = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) - 630, 260),
                (self.width, 120)
            ),
            text=sentence_challenge,
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@sentence_label")
        )
        
        sentence_text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=Rect(
                ((self.width / 2) - 490, 350),
                (1000, 80)
            ),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@sentence_text_entry")
        )   
        
        start_timer = time.time()
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_TEXT_ENTRY_CHANGED):
                    
                    if len(event.text) == len(sentence_challenge):
                        sentence = event.text
                        Finished(
                            rect=self.rect,
                            theme=self.theme,
                            music=self.music,
                            text_entry=event.text,
                            sentence=sentence_challenge,
                            timer=start_timer
                        ).start()
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            self.scroll_background(enabled=configure.ENABLED_SCROLLING_BACKGROUND)
            
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()
            

class Finished(engine.Engine):
    
    
    def __init__(self, rect: Rect, theme: str, music: bool, text_entry: str, sentence: str, timer: float):
        self.rect = rect
        self.width = rect.size[0]
        self.height = rect.size[1]
        
        self.theme = theme
        
        self.music = music
        
        self.text_entry = text_entry
        self.sentence = sentence
        self.timer = timer
        
        self.window_surface = pygame.display.set_mode(rect.size)
        self.background = pygame.Surface(rect.size)
        self.background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/core_background.png').convert()
        
        self.mini_sunshine_typing_logo = pygame.image.load(os.getcwd() + '/source/app/assets/image/mini_sunshine_typing_logo.png')
        self.result_background_image = pygame.image.load(os.getcwd() + '/source/app/assets/image/entry_name_background.png')
        
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
    
    def start(self) -> None:
        clock = pygame.time.Clock()
        is_running: bool = True
        
        total_time = time.time() - self.timer
        counter: int = 0
        for index, alpha in enumerate(self.sentence):
            try:
                if self.text_entry[index] == alpha:
                    counter += 1
            except:
                pass
        
        accuracy = (counter * 100) / len(self.sentence)
        words_per_minute = (len(self.text_entry) * 60) / (5 * total_time)
        
        fetch_rows = database_cursor.execute(
            "SELECT username FROM typing WHERE username = ?",
            (store.username.lower(),)
        ).fetchall()
        
        if len(fetch_rows).__eq__(0):
            database_cursor.execute(
                "INSERT INTO typing (username, wpm) VALUES (?, ?)", 
                (store.username.lower(), words_per_minute)
            )
            database.commit()
            
        elif len(fetch_rows).__eq__(1):
            database_cursor.execute(
                "UPDATE typing SET wpm = ? WHERE username = ?",
                (words_per_minute, store.username.lower())
            )
            database.commit()
            
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
        
        scoreboard_sign_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width - 170, -10),
                (150, 150)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@scoreboard_sign_button')
        )
        
        finished_label = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) - 640, 100),
                (self.width, 300)
            ),
            text="You have challenged the sentences",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@finished_label")
        )
        
        words_per_minute_background = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 230, 220),
                (265, 265)
            ),
            image_surface=self.result_background_image,
            manager=self.ui_manager,
        )
        
        accuracy_background = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 130, 220),
                (265, 265)
            ),
            image_surface=self.result_background_image,
            manager=self.ui_manager,
        )
        
        total_time_background = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                ((self.width / 2) - 490, 220),
                (265, 265)
            ),
            image_surface=self.result_background_image,
            manager=self.ui_manager,
        )
        
        words_per_minute_label = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) + 230, 185),
                (265, 265)
            ),
            text="WPM",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@result_title")
        )
        
        accuracy_label = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) - 130, 185),
                (265, 265)
            ),
            text="Accuracy",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@result_title")
        )
        
        total_time_label = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) - 490, 185),
                (265, 265)
            ),
            text="Total time",
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@result_title")
        )
        
        result_of_words_per_minute = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) + 230, 225),
                (265, 265)
            ),
            text="%d" % (words_per_minute),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@result_content")
        )
        
        result_of_accuracy = pygame_gui.elements.UILabel(
            relative_rect=Rect(
                ((self.width / 2) - 130, 225),
                (265, 265)
            ),
            text="%d" % (accuracy),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="@result_content")
        )
        
        if total_time > 9:
            result_of_total_time = pygame_gui.elements.UILabel(
                relative_rect=Rect(
                    ((self.width / 2) - 678, 225),
                    (640, 265)
                ),
                text="{:.0f} Secs".format(total_time),
                manager=self.ui_manager,
                object_id=ObjectID(object_id="@result_content")
            )
            
        else:
            result_of_total_time = pygame_gui.elements.UILabel(
                relative_rect=Rect(
                    ((self.width / 2) - 675, 225),
                    (640, 265)
                ),
                text="{:.0f} Secs".format(total_time),
                manager=self.ui_manager,
                object_id=ObjectID(object_id="@result_content")
            )
        
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (10, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@restart_button')
        )
        
        menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                ((self.width / 2) + 320, 580),
                (300, 120)
            ),
            text='',
            manager=self.ui_manager,
            object_id=ObjectID(object_id='@menu_button')
        )
        
        game_starter = Game(
            rect=self.rect,
            theme=self.theme,
            music=self.music 
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
        
        scoreboard_page = pages.Scoreboard(
            rect=self.rect, 
            theme=self.theme, 
            music=True,
        )
        
        restart_state: bool = False
        back_previous_page_state: bool = False
        
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type.__eq__(pygame.QUIT):
                    pygame.quit()
                    exit()
                    
                if event.type.__eq__(pygame_gui.UI_BUTTON_PRESSED):
                    if event.ui_element == restart_button:
                        restart_state = True
                        
                    if event.ui_element == menu_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                    
                        back_previous_page_state = True
                        
                    if event.ui_element == scoreboard_sign_button:
                        click_effect = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/effect/click.ogg')
                        click_effect.play()
                        
                        scoreboard_page.initialize()
                    
                self.ui_manager.process_events(event)
                
            self.ui_manager.update(time_delta)
            self.scroll_background(enabled=configure.ENABLED_SCROLLING_BACKGROUND)
            
            if restart_state:
                game_starter.start()
            
            if back_previous_page_state and self.music:
                typing_with_music_menu.run()
                
            if back_previous_page_state and not self.music:
                typing_without_music_menu.run()
            
            self.ui_manager.draw_ui(self.window_surface)
            
            pygame.display.update()