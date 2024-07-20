# build 2048 in python using pygame!!!
import json
import sys
import pygame
import random
import time
from twozerofoureight import Twozerofoureight
pygame.init()

#initial set up
# WIDTH = 400
# HEIGHT = 500
# screen = pygame.display.set_mode([WIDTH,HEIGHT])
# pygame.display.set_caption('2048')
# timer = pygame.time.Clock()
# fps = 60
# font = pygame.font.Font("freesansbold.ttf",24)


#2048 game color library

#game variables initialize

board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''

score = 0
file = open('python_2048/high_score','r')
init_high = int(file.readline())
file.close()
high_score = init_high


def main():
    global score,init_high,high_score,board_values,spawn_new,init_count,direction
    #main game loop
    run = True
    t_z_f_e = Twozerofoureight(score,init_high)

    while run:
        t_z_f_e.timer.tick(t_z_f_e.fps)
        t_z_f_e.screen.fill('gray')
        t_z_f_e.draw_board()
        t_z_f_e.draw_pieces(board_values)
        
        #給予初始化圖塊中的數字 def new_pieces()
        if spawn_new or init_count < 2:
            board_values, game_over = t_z_f_e.new_pieces(board_values)
            spawn_new  = False
            init_count += 1
        if direction != '':
            board_values = t_z_f_e.take_turn(direction,board_values)
            direction = ''
            spawn_new = True
        
        if game_over:
            t_z_f_e.draw_over()
            if high_score > init_high:
                file = open('python_2048/high_score','w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score
        
        #案右上角XX可離開遊戲
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:#這裡是指按鍵釋放(KEYDOWN:壓下按鍵,KEYUP:釋放按鍵)
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                
                if game_over:
                    if event.key == pygame.K_RETURN:
                        board_values = [[0 for _ in range(4)] for _ in range(4)] 
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ''
                        game_over = False
        
        if t_z_f_e.score > high_score:
            high_score = t_z_f_e.score      
        
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

