import pygame
from piece import *


class board():
    def __init__(self):
        self.board = []
        self.create_board()
        self.history = {}

    def print_board(self):
        print(self.board)
        
    def draw_board(self,win):
        win.fill((0,0,0))
        pygame.draw.polygon(win, (255,0,0), [(200,100),(200-150/(3**(1/2)),250),\
                                       (200+150/(3**(1/2)),250)])
        pygame.draw.polygon(win, (255,255,0),[(200-150/(3**(1/2)),250),\
                                              (200-2*150/(3**(1/2)),400),\
                                              (200-150/(3**(1/2)),550),\
                                              (200+150/(3**(1/2)),550),\
                                              (200+2*150/(3**(1/2)),400),\
                                              (200+150/(3**(1/2)),250)])
        pygame.draw.polygon(win, (0,0,128), [(200-150/(3**(1/2)),550)\
                                             ,(200+150/(3**(1/2)),550),\
                                             (200,700)])

        length = (4*150/(3**(1/2)))/8
        hori_x = [(200-2*150/(3**(1/2))+length*i) for i in range(1,8)]
        hori_y = 400
        # up to right
        diag1_x = [(200 + i*length/2) for i in range(1,8)]
        # up to left
        diag2_x = [(200 - i*length/2) for i in range(1,8)]
        
        diag3_x = diag2_x[::-1]
        diag1_y = [(100 + i * (3**(1/2))* length/2) for i in range(1,8)]
        diag2_y = diag1_y[::-1]
       

        pygame.draw.line(win, (0,0,0),(200-2*150/(3**(1/2)),hori_y),(200+2*150/(3**(1/2)),hori_y))

        diag_y_up = [(700 - i * (3**(1/2))* length/2) for i in range(1,8)]
        diag_y_up2 = diag_y_up[::-1]
        
        for i in range(7):
            pygame.draw.line(win, (0,0,0),(hori_x[i],hori_y),(diag1_x[i],diag1_y[i]))
            pygame.draw.line(win, (0,0,0),(hori_x[i],hori_y),(diag3_x[i],diag2_y[i]))
            pygame.draw.line(win, (0,0,0),(diag1_x[i],diag1_y[i]),(diag2_x[i],diag1_y[i]))

            pygame.draw.line(win, (0,0,0),(hori_x[i],hori_y),(diag1_x[i],diag_y_up[i]))
            pygame.draw.line(win, (0,0,0),(hori_x[i],hori_y),(diag3_x[i],diag_y_up2[i]))
            pygame.draw.line(win, (0,0,0),(diag1_x[i],diag_y_up[i]),(diag2_x[i],diag_y_up[i]))

    def draw_all(self,win):
        self.draw_board(win)
        
        for row in range(0,len(self.board)):
            for col in range(0,len(self.board[row])):
                piece = self.board[row][col]
                if piece!=0 and piece !=1:
                    piece.draw(win)

    def move(self, piece, row, col):
        if piece !=0:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)

    def get_piece(self,row,col):
         return self.board[row][col]


    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.direction == "down":
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.direction, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.direction, right))
            moves.update(self._traverse_left(row +1, min(row+3, 16), 1, piece.direction, left))
            moves.update(self._traverse_right(row +1, min(row+3, 16), 1, piece.direction, right))
            moves.update(self._traverse_hori_left(row, 0, -2, piece.direction, left))
            moves.update(self._traverse_hori_right(row, 16, 2, piece.direction, right))
            
            
        if piece.direction == "up":
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.direction, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.direction, right))
            moves.update(self._traverse_left(row +1, min(row+3, 16), 1, piece.direction, left))
            moves.update(self._traverse_right(row +1, min(row+3, 16), 1, piece.direction, right))
            moves.update(self._traverse_hori_left(row, 0, -2, piece.direction, left))
            moves.update(self._traverse_hori_right(row, 16, 2, piece.direction, right))
    
        return moves
        

    def _traverse_left(self, start, stop, step, direction, left, skipped=[]):
        
        
        moves = {}
        last = []
        for r in range(start, stop, step):
        # deal with special cases at the edge
            if left < 0:
                break
            if self.board[r][left]==1:

                break
            
            current = self.board[r][left]
           
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 16)
                    moves.update(self._traverse_left(r+step, row, step, direction, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, direction, left+1,skipped=last))
                    moves.update(self._traverse_hori_left(r, 0, -2, direction, left-1, skipped=last))
                    moves.update(self._traverse_hori_right(r, 16, 2, direction, left+1, skipped=last))
                break
            
            else:
                if last:
                    break
                else:
              
                    last = [current]

            left -= 1
        
        return moves

    def _traverse_hori_left(self, start, stop, step, direction, left, skipped=[]):
        moves = {}
        last = []
        left_hor = left-1
       
                    
        # you need to add an extra 1 otherwise it won't check if col==0
        for col in range(left_hor+1, stop, step):
            
            if self.board[start][col-1]==1:
                break
            
            current = self.board[start][col-1]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(start, col-1)] = last + skipped
                else:
                    moves[(start, col-1)] = last
                
                if last:
                    if direction == "up":
                        traverse_step = 1
                        reverse_step = -1
                        row = max(start+3, 0)
                    else:
                        traverse_step=-1
                        reverse_step  = 1
                        row = min(start-3, 16)
                    moves.update(self._traverse_left(start+traverse_step, row, traverse_step, direction, col-2,skipped=last))
                    moves.update(self._traverse_right(start+traverse_step, row, traverse_step, direction, col,skipped=last))
                    moves.update(self._traverse_left(start+reverse_step, row, reverse_step, direction, col-2,skipped=last))
                    moves.update(self._traverse_right(start+reverse_step, row, reverse_step, direction, col,skipped=last))
                    
                    moves.update(self._traverse_hori_left(start, 0, -2, direction, col-2, skipped=last))
                break
            
            else:
                if last:
                    break
                else:
              
                    last = [current]

            
        
        return moves

    def _traverse_hori_right(self, start, stop, step, direction, right, skipped=[]):
        moves = {}
        last = []
        right_hor = right+1
        # you need to substract an extra 1 otherwise it won't check if col==16
        for col in range(right_hor-1, stop, step):
            if self.board[start][col+1]==1:
                break
            
            current = self.board[start][col+1]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(start, col+1)] = last + skipped
                else:
                    moves[(start, col+1)] = last
                
                if last:
                    if direction == "up":
                        traverse_step = 1
                        reverse_step = -1
                        row = max(start+3, 0)
                    else:
                        traverse_step=-1
                        reverse_step = 1
                        row = min(start-3, 16)
                    moves.update(self._traverse_left(start+traverse_step, row, traverse_step, direction, col,skipped=last))
                    moves.update(self._traverse_right(start+traverse_step, row, traverse_step, direction, col+2,skipped=last))
                    moves.update(self._traverse_left(start+reverse_step, row, reverse_step, direction, col,skipped=last))
                    moves.update(self._traverse_right(start+reverse_step, row, reverse_step, direction, col+2,skipped=last))
                    moves.update(self._traverse_hori_right(start, 16, 2, direction, col+2, skipped=last))
                break
            
            else:
                if last:
                    break
                else:
              
                    last = [current]

            
        
        return moves

    

    


    def _traverse_right(self, start, stop, step, direction, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
        # so that it won't go off the limit in special cases
            if right > 16:
                break
            if self.board[r][right]==1:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 16)
                    moves.update(self._traverse_left(r+step, row, step, direction, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, direction, right+1,skipped=last))
                    moves.update(self._traverse_hori_left(r, 0, -2, direction, right-1, skipped=last))
                    moves.update(self._traverse_hori_right(r, 16, 2, direction, right+1, skipped=last))
                break
           
            
            else:
                if last:
                    break
                else:
              
                    last = [current]
            right += 1
        
        return moves        
        
    
                

    def create_board(self):
        for i in range(17): 
            self.board.append([])
            for j in range(17):
                self.board[i].append(1)


        for j in range(5):
            if j==0:
                self.board[j][8]= piece(j,8,(255,255,255),"up")
            elif j==2:
                self.board[j][6]=piece(j,6,(255,255,255),"up")
                self.board[j][8]=piece(j,8,(255,255,255),"up")
                self.board[j][10]=piece(j,10,(255,255,255),"up")
                
            elif j ==4:
                self.board[j][4]=piece(j,4,(255,255,255),"up")
                self.board[j][6]=piece(j,6,(255,255,255),"up")
                self.board[j][8]=piece(j,8,(255,255,255),"up")
                self.board[j][10]=piece(j,10,(255,255,255),"up")
                self.board[j][12]=piece(j,12,(255,255,255),"up")
                
            elif j==1:
                self.board[j][7]=piece(j,7,(255,255,255),"up")
                self.board[j][9]=piece(j,9,(255,255,255),"up")
            elif j==3:
                self.board[j][5]=piece(j,5,(255,255,255),"up")
                self.board[j][7]=piece(j,7,(255,255,255),"up")
                self.board[j][9]=piece(j,9,(255,255,255),"up")
                self.board[j][11]=piece(j,11,(255,255,255),"up")

        
        for m in range(12,17):
            if m == 12:
                self.board[m][4]=piece(m,4,(255,255,255),"down")
                self.board[m][6]=piece(m,6,(255,255,255),"down")
                self.board[m][8]=piece(m,8,(255,255,255),"down")
                self.board[m][10]=piece(m,10,(255,255,255),"down")
                self.board[m][12]=piece(m,12,(255,255,255),"down")
               
            elif m== 13:
                self.board[m][5]=piece(m,5,(255,255,255),"down")
                self.board[m][7]=piece(m,7,(255,255,255),"down")
                self.board[m][9]=piece(m,9,(255,255,255),"down")
                self.board[m][11]=piece(m,11,(255,255,255),"down")
                
            elif m ==14:
                self.board[m][6]=piece(m,6,(255,255,255),"down")
                self.board[m][8]=piece(m,8,(255,255,255),"down")
                self.board[m][10]=piece(m,10,(255,255,255),"down")
            
            elif m==15:
                self.board[m][7]=piece(m,7,(255,255,255),"down")
                self.board[m][9]=piece(m,9,(255,255,255),"down")
                
            elif m==16:
                self.board[m][8]=piece(m,8,(255,255,255),"down")

        for i in range(6):
            self.board[5][3+2*i] = 0
        for i in range(7):
            self.board[6][2+2*i] = 0
        for i in range(8):
            self.board[7][1+2*i] = 0
        for i in range(9):
            self.board[8][2*i] = 0
        for i in range(8):
            self.board[9][1+2*i] = 0
        for i in range(7):
            self.board[10][2+2*i] = 0
        for i in range(6):
            self.board[11][3+2*i] = 0
        
                
    def winner(self):
        winner = None
        count_green = 0
        count_white = 0
        for i in range(17):
            for j in range(17):
                piece = self.get_piece(i,j)
                if piece!=0 and piece!=1 and piece.direction=="down" and i<=4:
                    count_green += 1
                elif piece!=0 and piece!=1 and piece.direction=="up" and i>=12:
                    count_white +=1

        if count_green == 15:
            winner = "down"
        elif count_white == 15:
            winner = "up"
          
                    
                
        
        return winner

    def early_stop(self):
        winner = None
        count_upside=0
        count_downside =0
        for row in range(8):
            for col in range(0,len(self.board[row])):
                piece = self.get_piece(row,col)
                if piece!=0 and piece!=1 and piece.direction=="down":
                    count_upside+=1
        
        for row in range(8,17):
            for col in range(0,len(self.board[row])):
                piece = self.get_piece(row,col)
                if piece!=0 and piece!=1 and piece.direction=="up":
                    count_downside+=1

        if count_upside>count_downside:
            winner="down"
        
        elif count_downside>count_upside:
            winner="up"

        return winner
          
