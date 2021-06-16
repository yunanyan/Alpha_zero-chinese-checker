from board import board
from game import game
import pygame

def update(game,win):
    game.gameboard.draw_all(win)
    draw_valid_moves(game.valid_moves,win)
    pygame.display.update()

def draw_valid_moves(moves,win):
    for move in moves:
        row, col = move
        length = (4*150/(3**(1/2)))/8
        y = 100+(row)*(3**(1/2))* length/2
        x = 200-2*150/(3**(1/2))+col*(length/2)
        pygame.draw.circle(win, (0,0,255),(x,y),8)

FPS = 60

WIN = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    length = (4*150/(3**(1/2)))/8
    x,y = pos
    row = round((y-100)/(((3**(1/2))* length/2)))
    col = round((x-(200-2*150/(3**(1/2))))/(length/2))
    return row, col

def main():
    
    run = True
    clock = pygame.time.Clock()
    mygame = game()
    
    
    while run:
        clock.tick(FPS)
        if mygame.winner() != None:
            print(mygame.winner())
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                row1, col1 = get_row_col_from_mouse(pos1)
                mygame.select(row1,col1)
                
    

        update(mygame,WIN) 
    pygame.quit()


main()
