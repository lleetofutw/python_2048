import json
import sys
import pygame
import random
import time
pygame.init()

WIDTH = 400
HEIGHT = 500

class Twozerofoureight: #2048
    def __init__(self,score,high_score):
        self.screen = pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption('2048')
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font("freesansbold.ttf",24)

        f = open('python_2048/2048_color.json')
        self.colors = json.load(f)
        f.close()

        self.score = score
        self.high_score = high_score
        


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

    def new_pieces(self,board):
        count = 0
        full = False
        # python any()用法:https://www.freecodecamp.org/chinese/news/python-any-and-all-functions-explained-with-examples/
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0,3)
            col = random.randint(0,3)
            if board[row][col] == 0:
                count += 1
                if random.randint(1,10) == 10:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
        if count < 1:
            full = True      
                                
        return board,full
    

    def take_turn(self,direc,board):
        merged = [[False for _ in range(4)] for _ in range(4)]
        if direc == 'UP':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            if board[q][j] == 0:
                                shift += 1
                        if shift >0:
                            board[i -shift][j] = board[i][j]
                            board[i][j] = 0
                        if board[i - shift - 1][j] == board[i-shift][j] and not merged[i - shift][j] and not merged[i - shift -1][j]:
                            board[i - shift - 1][j] *= 2
                            self.score += board[i - shift - 1][j]
                            board[i - shift][j] = 0
                            merged[i - shift -1][j] = True
                            
        elif direc == 'DOWN':
            for i in range(3):
                for j in range(4):
                    shift = 0
                    for q in range(i + 1):
                        if board[3 - q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[2 - i + shift][j] = board[2 - i][j]
                        board[2 - i][j] = 0
                    if 3 - i + shift <= 3:
                        if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                            board[3 - i + shift][j] *= 2
                            self.score += board[3 - i + shift][j]
                            board[2 - i + shift][j] = 0
                            merged[3 - i + shift][j] = True
        elif direc == 'LEFT':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j - shift] =board[i][j]
                        board[i][j] = 0
                    if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - i] and not merged[i][j - shift]:
                        board[i][j - shift -1] *= 2
                        self.score += board[i][j - shift -1]
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True
                    
        elif direc == 'RIGHT':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][3 - q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][3 -j + shift] = board[i][3 - j]
                        board[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                            board[i][4 -j +shift] *= 2
                            self.score += board[i][4 -j +shift]
                            board[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True

        return board
    
    def draw_over(self):
        pygame.draw.rect(self.screen,'black',[50,50,300,100],0,10)
        game_over_text1 = self.font.render('Game Over!',True,'white')
        game_over_text2 = self.font.render('Press Enter to Restart',True,'white')
        self.screen.blit(game_over_text1,(130,65))
        self.screen.blit(game_over_text2,(70,105))