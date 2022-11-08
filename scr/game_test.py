import pygame as pg
from sys import exit
import numpy as np
import os
import ntpath
from numba import njit

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
    res_horizontal = 480
    half_res_vertical = 400

    #ângulo de visão do jogador
    fov = res_horizontal/60
    #posiçao inicial do jogador
    posx, posy, rot = 3, 3, 180
    
    frame = np.random.uniform(0,1, (res_horizontal, half_res_vertical*2, 3))

    #mapa
    tamanho = 25
    mapa = (
        [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], 
        [1,0,0,0,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,0,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,0,1,1,3,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,2,2],
        [1,0,0,0,1,1,2,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,2,2],
        [1,0,0,1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,2,2],
        [2,0,0,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,2,0,0,0,0,2,2],
        [2,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [2,0,0,0,0,0,0,0,2,1,0,0,0,1,0,0,0,1,2,0,0,0,0,2,2],
        [2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,2,2,2,2],
        [2,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [2,0,0,0,0,0,0,0,2,1,0,0,0,1,0,0,0,1,2,0,0,0,0,2,2],
        [2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,2,0,0,0,0,2,2],
        [1,0,0,2,2,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,2,0,0,0,0,2,2],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2])

    #texturas
    ceu = pg.image.load('textures/sky2.png')
    ceu = pg.surfarray.array3d(pg.transform.scale(ceu, (360, half_res_vertical*2)))
    floor = pg.surfarray.array3d(pg.image.load('textures/floor2.png'))
    wall = pg.surfarray.array3d(pg.image.load('textures/greystone.jpg'))
    wall2 = pg.surfarray.array3d(pg.image.load('textures/bluestone.png'))
    wall3 = pg.surfarray.array3d(pg.image.load('textures/obg.png'))
    '''wall4 = pg.surfarray.array3d(pg.image.load('textures/wood.png'))
    wall5 = pg.surfarray.array3d(pg.image.load('textures/redbrick.png'))
    wall6 = pg.surfarray.array3d(pg.image.load('textures/eagle.png'))'''


    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        frame = numba_frame(floor, ceu, posx, posy, rot, frame, res_horizontal,  half_res_vertical, fov, mapa, tamanho, wall, wall2, wall3)

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

#otimizaçao do código usando numba (faz milagre essa porra)
@njit()
def numba_frame(floor, ceu, posx, posy, rot, frame, res_horizontal,  half_res_vertical, fov, mapa, tamanho, wall, wall2, wall3):
    for i in range(res_horizontal):
            rot_i = rot + np.deg2rad(i/fov - 30)
            sin, cos, cos_correcao = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/fov-30))
            frame[i][:] = ceu[int(np.rad2deg(rot_i)%359)][:]/255

            for j in range(half_res_vertical):
                n = (half_res_vertical/(half_res_vertical-j))/cos_correcao
                x, y = posx + cos*n, posy + sin*n
                xfloor, yfloor = int(x*2%1*299), int(y*2%1*299)

                #Geraçao das paredes textura 1
                if mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 1:
                    h = half_res_vertical - j
                    if x%1<0.019 or x%1>=0.981:
                        xfloor = yfloor
                    yfloor = np.linspace(0,598, h*2)%299

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall[xfloor][int(yfloor[k])]/255
                    break

                #Geraçao das paredes textura 2    
                elif mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 2:
                    h = half_res_vertical - j
                    if x%1<0.015 or x%1>=0.985:
                        xfloor = yfloor
                    yfloor = np.linspace(0,598, h*2)%299

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall2[xfloor][int(yfloor[k])]/255
                    break
                #Chão 
                
                #Geraçao das paredes textura 2    
                elif mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 3:
                    h = half_res_vertical - j
                    if x%1<0.015 or x%1>=0.985:
                        xfloor = yfloor
                    yfloor = np.linspace(0,299, h*2)%299

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall3[xfloor][int(yfloor[k])]/255
                    break
                #Chão 
                else:
                    frame[i][half_res_vertical*2-j-1] = floor[xfloor][yfloor]/255
                #Geraçao das paredes textura 3    
                '''if mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 3:
                    h = half_res_vertical - j
                    if x%1<0.1 or x%1>0.9:
                        xfloor = yfloor
                    yfloor = np.linspace(0,64, h*2)%64

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall2[xfloor][int(yfloor[k])]/255
                    break

                #Geraçao das paredes textura 3    
                if mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 3:
                    h = half_res_vertical - j
                    if x%1<0.1 or x%1>0.9:
                        xfloor = yfloor
                    yfloor = np.linspace(0,64, h*2)%64

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall2[xfloor][int(yfloor[k])]/255
                    break

                #Geraçao das paredes textura 4    
                if mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 4:
                    h = half_res_vertical - j
                    if x%1<0.1 or x%1>0.9:
                        xfloor = yfloor
                    yfloor = np.linspace(0,64, h*2)%64

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall2[xfloor][int(yfloor[k])]/255
                    break

                #Geraçao das paredes textura 5    
                if mapa[int(x)%(tamanho-1)][int(y)%(tamanho-1)] == 5:
                    h = half_res_vertical - j
                    if x%1<0.1 or x%1>0.9:
                        xfloor = yfloor
                    yfloor = np.linspace(0,64, h*2)%64

                    for k in range(h*2):
                        frame[i][half_res_vertical - h + k] = wall2[xfloor][int(yfloor[k])]/255
                    break'''
    return frame

game()