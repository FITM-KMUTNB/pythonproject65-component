import os
import pygame
from pygame.locals import *
from pygame import mixer
from sys import exit

WIDTH: int = 1920
HEIGHT: int = 1080

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load('./src/images/root_background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

mixer.init()
mixer.music.load('./src/music/root_music_background.mp3')
mixer.music.play()
mixer.music.set_volume(0.2)

while True:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pygame.display.update()

pygame.quit()
