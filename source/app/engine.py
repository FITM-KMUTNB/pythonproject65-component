import pygame
import os

class Engine:
    pygame.init()
    pygame.mixer.init()
    
    giga_chad = pygame.mixer.Sound(os.getcwd() + '/source/app/assets/audio/giga_chad.ogg')
    pygame.mixer.Channel(1).play(giga_chad, loops=-1, fade_ms=10)