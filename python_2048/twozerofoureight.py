import json
import sys
import pygame
import random
import time
pygame.init()

WIDTH = 400
HEIGHT = 500

class Twozerofoureight: #2048
    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption('2048')
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font("freesansbold.ttf",24)

        f = open('2048_color.json')
        self.colors = json.load(f)
        f.close()
        
        
        #game variables initialize
        self.score = 0
        file = open('high_score','r')
        init_high = int(file.readline())
        self.high_score = init_high

    def get_colors(self,index:str):
        pixel = (self.colors["colors"][index][0],self.colors["colors"][index][1],self.colors["colors"][index][2])
        return pixel
    
    def draw_board(self):
        bg = self.get_colors('bg')
        pygame.draw.rect(self.screen,bg,[0,0,400,400],0,10)
        score_text = self.font.render(f'Score: {self.score}',True,'black')
        high_score_text = self.font.render(f'High Score: {self.high_score}',True,'black')
        self.screen.blit(score_text,(10,410))
        self.screen.blit(high_score_text,(10,450))
        
    
    def draw_pieces(self,board):
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value > 8:
                    value_color = self.get_colors('light_text')
                else:
                    value_color = self.get_colors('dark_text')
                if value <= 2048:
                    # color = colors[value]
                    color = self.get_colors(str(value))
                else:
                    color = self.get_colors('other')
                pygame.draw.rect(self.screen,color,[j*95+20,i*95+20,75,75],0,5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font("freesansbold.ttf",48 - (5*value_len))
                    value_text = font.render(str(value),True,value_color)
                    text_rect = value_text.get_rect(center = (j*95+57,i*95+57))
                    self.screen.blit(value_text,text_rect)
                    pygame.draw.rect(self.screen,'black',[j*95+20,i*95+20,75,75],2,5)