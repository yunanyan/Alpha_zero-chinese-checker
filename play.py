from board import board
from game import game
from mcts_alpha import MCTSPlayer
from network import policyvaluenet
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

    
def start_play(player2, start_player = "up"):
    if start_player not in ("up","down"):
        raise Exception("start player must be either up or down")

   
    player1 = "human player"
    player2.set_player_ind("down")
    players = {"up": player1, "down": player2}

    FPS = 60

    WIN = pygame.display.set_mode((400, 800))
    pygame.display.set_caption('Checkers')
    def get_row_col_from_mouse(pos):
        length = (4*150/(3**(1/2)))/8
        x,y = pos
        row = round((y-100)/(((3**(1/2))* length/2)))
        col = round((x-(200-2*150/(3**(1/2))))/(length/2))
        return row, col
    
    run = True
    clock = pygame.time.Clock()
    mygame = game()

    while run:
        clock.tick(FPS)
        game_winner = mygame.winner()
        if game_winner:
            if game_winner == "up":
                print("player 1 wins")
            if game_winner == "down":
                print("player 2 wins")
            return game_winner
        current_player = mygame.get_current_player()
        player_in_turn = players[current_player]
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and player_in_turn==player1:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                
                mygame.select(row,col)
            if event.type == pygame.MOUSEBUTTONDOWN and player_in_turn==player2:
                move = player_in_turn.get_action(mygame)
              
                mygame.select(move[0][0],move[0][1])
                
                mygame.select(move[1][0],move[1][1])

        update(mygame,WIN)
    pygame.quit()


def main():
    best_policy = policyvaluenet()
    mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)
    start_play(mcts_player,start_player = "up" )

main()

        
                    
        
