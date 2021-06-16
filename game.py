from board import board
from piece import *
import numpy as np
import pygame

class game():
    def __init__(self):
        self._init()
       
        self.last_move =None

    def _init(self):
        self.gameboard = board()
        # up go first/player1 go first
        self.turn = "up"
        self.valid_moves = {}
        self.selected = None

    def reset(self):
        self._init()

    def winner(self):
        return self.gameboard.winner()


    
    def get_current_player(self):
        return self.turn

    # I need a dictionary that maps all possible moves to the x,y of who that move belongs to
    def get_all_valid_moves(self):
        total_valid_moves = []
        for row in range(17):
            for col in range(17):
                valid_moves = None 
                if self.gameboard.board[row][col]!=1 and self.gameboard.board[row][col]!=0:
                    if self.gameboard.board[row][col].direction == self.turn:
                        valid_moves = self.gameboard.get_valid_moves(self.gameboard.board[row][col])
                if valid_moves:
                    for key in valid_moves.keys():
                        # [((current row,col),(next row,col))]
                        total_valid_moves.append(((row,col),key))
        return total_valid_moves

    def select(self,row,col):
        # if there is something selected, then move it to (row,col), if already occupied, reselect the occupied one.
        if self.selected:
            result = self._move(row, col)
            if not result:
                # reset selected
                self.selected = None
                # call this method again to reselect
                self.select(row, col)
        else: # select the piece at (row, col)
            piece = self.gameboard.get_piece(row,col)
            if piece !=0 and piece!= 1 and piece.direction == self.turn:
                self.selected = piece
                self.valid_moves = self.gameboard.get_valid_moves(piece)
                
                return True
        return False

    def _move(self,row,col):
        # check if the destination position has been occupied & if the move is valid
        piece = self.gameboard.get_piece(row,col)
        
        if self.selected and piece ==0 and (row,col) in self.valid_moves:
            prev_row = self.selected.row
            prev_col = self.selected.col
            self.gameboard.move(self.selected, row, col)
            self.change_turn()
            self.last_move = ((prev_row, prev_col),(row, col))
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == "up":
            self.turn = "down"
        else:
            self.turn = "up"

   

    def get_currentstate(self):
        """
        two layers for now: location of player1's figures; location of player2's figures
        one layer for last move
        one layer for who makes last move
        """
        square_state = np.zeros([4,17,17])
        layer1 = []
        layer2 = []
        for row in range(17):
            for col in range(17):
                if self.gameboard.board[row][col] != 0 and self.gameboard.board[row][col] !=1:
                    if self.gameboard.board[row][col].direction == "up":
                        
                        layer1.append((row,col))
        for row in range(17):
            for col in range(17):
                if self.gameboard.board[row][col] != 0 and self.gameboard.board[row][col] !=1:
                    if self.gameboard.board[row][col].direction == "down":
                        layer2.append((row,col))
        for item in layer1:
            square_state[0][item[0],item[1]]=1.0
        for item in layer2:
            square_state[1][item[0],item[1]]=1.0
        # where does the last move end
        # the first time will be None. So skip it
        if self.last_move!= None:
            square_state[2][self.last_move[1][0], self.last_move[1][1]]=1.0

        if self.turn == "up":
            square_state[3][:,:]=1.0 # 1.0 if it is the start player's turn

        return square_state[:, ::-1, :]
                        

    def start_self_play(self,player, temp=1e-3, show=None):
        
        if show is None:
            step=0
            states, mcts_probs, current_players = [], [], []
            while True:
                step+=1
                move, move_probs = player.get_action(self,
                                                     temp=temp,
                                                     return_prob=1)
               

                self.last_move=move
                # store the data
                states.append(self.get_currentstate())
                mcts_probs.append(move_probs)
                current_players.append(self.turn)
              
                
                # perform a move
                self.select(move[0][0],move[0][1])
                        
                self.select(move[1][0],move[1][1])
                
                winner = self.winner()
                if winner!=None:
                    winners_z = np.zeros(len(current_players))
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                    # reset MCTS root node
                    player.reset_player()
                    
                    return winner, zip(states, mcts_probs, winners_z)
                else:
                    # if no winner but 50 step has ocurred, stop early
                    if step>=50:
                        temp_winner = self.gameboard.early_stop()
                        if temp_winner!=None:
                            winners_z = np.zeros(len(current_players))
                            winners_z[np.array(current_players) == temp_winner] = 1.0
                            winners_z[np.array(current_players) != temp_winner] = -1.0
                            # reset MCTS root node
                            player.reset_player()
                            return winner, zip(states, mcts_probs, winners_z)

        else:
            
            step=0
            states, mcts_probs, current_players = [], [], []
            while True:
                step+=1
                move, move_probs = player.get_action(self,
                                                     temp=temp,
                                                     return_prob=1)
               

                self.last_move=move
                # store the data
                states.append(self.get_currentstate())
                mcts_probs.append(move_probs)
                current_players.append(self.turn)
                
                
                # perform a move
                self.select(move[0][0],move[0][1])
                        
                self.select(move[1][0],move[1][1])
                self.gameboard.draw_all(show)
                for move in self.valid_moves:
                    row, col = move
                    length = (4*150/(3**(1/2)))/8
                    y = 100+(row)*(3**(1/2))* length/2
                    x = 200-2*150/(3**(1/2))+col*(length/2)
                    pygame.draw.circle(win, (0,0,255),(x,y),8)
                pygame.display.update()

                
                winner = self.winner()
                if winner!=None:
                    winners_z = np.zeros(len(current_players))
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                    # reset MCTS root node
                    player.reset_player()
                    
                    return winner, zip(states, mcts_probs, winners_z)

                else:
                    # if no winner but 50 step has ocurred, stop early
                    if step>=50:
                        temp_winner = self.gameboard.early_stop()
                        if temp_winner!=None:
                            winners_z = np.zeros(len(current_players))
                            winners_z[np.array(current_players) == temp_winner] = 1.0
                            winners_z[np.array(current_players) != temp_winner] = -1.0
                            # reset MCTS root node
                            player.reset_player()
                            return winner, zip(states, mcts_probs, winners_z)


                
                
    
                
            
            
        
    
    
    
    
   
    


    
        
        
    
        
