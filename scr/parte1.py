import pygame as pg
from sys import exit
import numpy as np

pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('Yuri me da 10 pfv')
#limitando o fps 
clock = pg.time.Clock()
running = True

superficie = pg.Surface((100, 200))
superficie.fill('lightblue')

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #frame = np.random.uniform(0,1, (128, 72, 3))
    #surf = pg.surfarray.make_surface(frame*255)
    #surf = pg.transform.scale(surf, (1280, 720))
    screen.blit(superficie, (100, 200))

    pg.display.update()
    clock.tick(60)

pg.quit()
exit()
