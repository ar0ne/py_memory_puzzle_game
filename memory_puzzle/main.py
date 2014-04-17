#! /usr/bin/env python
"""
Memory puzzle 
author: Serg Ar[]ne 
e-mail: ja_he@mail.ru
"""

import sys, pygame, random

GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
CYAN = ( 120, 120, 255)

width = height = 70
margin = 10
N = 4
FONTSIZE = 45
FPS = 30 


def Won(scr, N, size,font):
    #if size == N*N:
    if size == size:
        pygame.draw.rect(scr, CYAN, [0, (N-1)*height/2, N*(width+margin)+margin , height*1.5])
        text = font.render("You are won!",True, ORANGE)
        scr.blit(text, [(N-1)*(width+margin)/2, (N-1)*(height+margin)/2]) 
                    


def Game_main():
    pygame.init()
    
    pygame.display.set_caption("Memory puzzle")
    SIZE = [(width+margin)*N + margin, (height+margin)*N + margin]
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, FONTSIZE)
     
    table = [[0 for i in range(N)] for i in range(N)]      # init list of pole NxN 
    
    secret_list = [] 
    it = 0
    while it < N*N/2:
        i = random.randrange(33, 126)       # ascii 
        if not chr(i) in secret_list:
            secret_list.append(chr(i)) 
            it += 1 
    
    secret_list *= 2        # make pairs for elements 
    
    it = len(secret_list)
    while it != 0:          # randomly adding elements to table[]
        for i in range(N):
            for j in range(N):
                it -= 1
                index = random.randrange(len(secret_list))
                table[i][j] = secret_list[index]
                secret_list.pop(index)
          
    
    screen.fill(GRAY)
    
    for i in range(N):
        for j in range(N):
            pygame.draw.rect(screen, ORANGE, [j * (width + margin) + margin, i * (height + margin) + margin, width, height])
 
    x = y = 0
    last = []
    opened = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                x /= (width + margin)
                y /= (height + margin)
                
                if not [y,x] in opened:    # if don't click to the cells what was opened early
                    pygame.draw.rect(screen, WHITE, [x * (width + margin) + margin, y * (height + margin) + margin, width, height])
                    text = font.render(str(table[y][x]),True, ORANGE)
                    screen.blit(text, [x * (width + margin) + width/2 ,y * (height + margin) + height/2 - FONTSIZE/5 ]) 
                    
            if event.type == pygame.MOUSEBUTTONUP:             

                if not [y,x] in opened:    # if don't click to the cells what was opened early
                    pygame.time.wait(500)
                    
                    if len(last) != 0:      # if it's not a first click
                        if last[0] != [y, x]:
                            if table[y][x] != table [ last[0][0] ][ last[0][1] ]:       # if don't equal last choose
                                pygame.draw.rect(screen, ORANGE, [x * (width + margin) + margin, y * (height + margin) + margin, width, height])
                            
                            elif table[y][x] == table [ last[0][0] ][ last[0][1] ] and last[0] != [y,x]:
                                pygame.draw.rect(screen, WHITE, [last[0][1] * (width + margin) + margin, last[0][0] * (height + margin) + margin, width, height])
                                text = font.render(str(table[last[0][0]][last[0][1]]),True, ORANGE)
                                screen.blit(text, [last[0][1] * (width + margin) + width/2 ,last[0][0] * (height + margin) + height/2 - FONTSIZE/5]) 
                                opened.append(last[0])    # add to list of opened cells
                                opened.append([y,x])
                            last[0] = [y,x]
                        
                    else:       # if don't click early
                        last.append([y, x])
                        pygame.draw.rect(screen, ORANGE, [x * (width + margin) + margin, y * (height + margin) + margin, width, height])
    
        Won(screen, N, len(opened),font)
        pygame.display.flip()
        clock.tick(FPS)

#########################################
if __name__ == '__main__':
    Game_main()
    