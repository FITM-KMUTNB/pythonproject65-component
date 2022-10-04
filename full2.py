import pygame
pygame.init()
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
white=pygame.color.Color('#FFFFFF')
finished=False
while not finished:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()