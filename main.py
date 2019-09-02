#! /usr/bin/env python

import sys, pygame, random

pygame.init()

GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
FIOLET = ( 120, 120, 255)

width = height = 70
margin = 10
N = 6
FONTSIZE = 45
FPS = 30 
WINDOWIDTH = 0
WINDOWHEIGHT = 0

#
# TODO: Add Timer for game loop
#

def Won(scr, N, size, font):
    if size == N*N:
        pygame.draw.rect(scr, FIOLET, [0, WINDOWHEIGHT/2 - (height+margin)/2, WINDOWIDTH , WINDOWHEIGHT/(N-1)])
        text = font.render("You are won!",True, ORANGE)
        scr.blit(text, [margin, WINDOWHEIGHT/2 ])
        pygame.display.update()
        pygame.time.wait(1500)
        Start_menu()    
        return
        

def Start_menu():
    
    global N, FPS, FONTSIZE
    
    clock = pygame.time.Clock() 
    font = pygame.font.Font(None, FONTSIZE)
    pygame.display.set_caption("Memory puzzle by ar[]ne")
    screen = pygame.display.set_mode([500, 250])
    screen.fill(GRAY)
  
    idx = [4, 6, 8]
    pos_squares = []
    
    for i in range(len(idx)):       # add position of buttons to list
        pos_squares.append([i * 2 * width + width, height/2 , width, height])
        pygame.draw.rect(screen, ORANGE,  pos_squares[i])
        pos_squares[i][2] += pos_squares[i][0]      # get right corner
        pos_squares[i][3] += pos_squares[i][1]      # get botttom
        text = font.render(str(idx[i]) + 'x' + str(idx[i]),True, WHITE)
        screen.blit(text, [i * 2 * width+width*1.15, height ]) 
        
        
    text = font.render("Choose size of the field" ,True, WHITE)
    screen.blit(text, [width, height*2 ]) 
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:        
                pos = pygame.mouse.get_pos()
                for i in range(len(pos_squares)):       # if user click in the button-square
                    if pos_squares[i][0] < pos[0] < pos_squares[i][2]  and pos_squares[i][1] < pos[1] < pos_squares[i][3]:
                        N = idx[i]      # set global SIZE of field
                        Game_main()
                        return
            
        pygame.display.flip()
        clock.tick(FPS)



def Game_main():
    global WINDOWIDTH, WINDOWHEIGHT, FONTSIZE, FPS
       
    clock = pygame.time.Clock() 
    font = pygame.font.Font(None, FONTSIZE) 
    pygame.display.set_caption("Memory puzzle by ar[]ne")
   
    WINDOWIDTH = (width+margin)*N + margin
    WINDOWHEIGHT = (height+margin)*N + margin

    screen = pygame.display.set_mode([WINDOWIDTH, WINDOWHEIGHT] )
    
    table = [[0 for i in range(N)] for i in range(N)]      # init list of field NxN 
    
    x = y = -1
    last = []
    opened = []
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
                        else:       # if not a first and equal last choose
                            pygame.draw.rect(screen, ORANGE, [x * (width + margin) + margin, y * (height + margin) + margin, width, height])
                    else:       # if don't click early
                        last.append([y, x])
                        pygame.draw.rect(screen, ORANGE, [x * (width + margin) + margin, y * (height + margin) + margin, width, height])
    
        Won(screen, N, len(opened),font)
        pygame.display.flip()
        clock.tick(FPS)

#########################################
if __name__ == '__main__':  
    Start_menu()
        
    
