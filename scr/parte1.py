import pygame as pg
from sys import exit
import numpy as np
import os
import ntpath

if __name__ == "__main__":
    head, tail = ntpath.split(os.path.realpath(__file__))
    os.chdir(head)

def game():
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Yuri me da 10 pfv')
    #limitando o fps usando o pg.time.Clock
    clock = pg.time.Clock()
    running = True
    res_horizontal = 216
    half_res_vertical = 180

    #ângulo de visão do jogador
    fov = res_horizontal/60
    #posiçao inicial do jogador
    posx, posy, rot = 0, 0, 0
    frame = np.random.uniform(0,1, (res_horizontal, half_res_vertical*2, 3))

    #texturas
    ceu = pg.image.load('textures/sky.jpg')
    ceu = pg.surfarray.array3d(pg.transform.scale(ceu, (360, half_res_vertical*2)))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        for i in range(res_horizontal):
            rot_i = rot + np.deg2rad(i/fov - 30)
            sin, cos, cos_correcao = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/fov - 30))
            frame[i][:] = ceu[int(np.rad2deg(rot_i)%360)][:]/255

            for j in range(half_res_vertical):
                n = (half_res_vertical/(half_res_vertical-j))/cos_correcao
                x, y = posx + cos*n, posy + sin*n

                if int(x)%2 == int(y)%2:
                    frame[i][half_res_vertical*2-j-1] = [0, 0, 0]
                else:
                    frame[i][half_res_vertical*2-j-1] = [1, 1, 1]
        
        surf = pg.surfarray.make_surface(frame*255)
        surf = pg.transform.scale(surf, (1280, 720))
        screen.blit(surf, (0, 0))

        pg.display.update()
        
        posx, posy, rot = movimentacao(posx, posy, rot, pg.key.get_pressed())
        #Número máximo de fps
        clock.tick(60)
    pg.quit()
    exit()

def movimentacao(posx, posy, rot, keys):
    #A e D diminuem e aumentam a rotação respectivamente
    if keys[ord('a')]:
        rot = rot - 0.08

    if keys[ord('d')]:
        rot = rot + 0.08
    
    #W soma o cosseno da rotação à posição x e o seno da rotação à posição y
    if keys[ord('w')]:
        posx, posy = posx + np.cos(rot)*0.12, posy + np.sin(rot)*0.12

    #S diminui o cosseno da rotação à posição x e o seno da rotação à posição y
    if keys[ord('s')]:
        posx, posy = posx - np.cos(rot)*0.12, posy - np.sin(rot)*0.12
    
    return posx, posy, rot

game()