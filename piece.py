import pygame

class piece():
    def __init__(self, row, col, color, direction):
        self.radius = 8
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calxy()
        self.direction = direction

    def calxy(self):
        length = (4*150/(3**(1/2)))/8
        self.y = 100+(self.row)*(3**(1/2))* length/2
        self.x = 200-2*150/(3**(1/2))+self.col*(length/2)

    def draw(self,win):
        if self.direction == "up":
            pygame.draw.circle(win, (255,255,255), (self.x, self.y), self.radius)
        if self.direction == "down":
            pygame.draw.circle(win, (11,250,75), (self.x, self.y), self.radius)


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calxy()


    
        
