import pygame
from stack import Stack

class Hanoi:
    def __init__(self,screen, towers: Stack, rings=3):
        self.screen = screen
        self.towers = towers


        self.start = Stack()
        for val in range(rings):
            ring = Ring(self.screen,val,self.towers.index(0))
            self.start.insert(ring)
        self.towers.index(0).stack = self.start.copy()
    
    def update(self):
        for i in self.towers:
            i.update()

class Tower:
    def __init__(self, screen,stack):
        self.screen = screen
        self.stack = stack
        self.image = pygame.image.load('images/game/tower.png')
        self.image_rect = self.image.get_rect()
    
    def update(self):
        for i in self.stack:
            i.update()

        self.screen.blit(self.image, self.image_rect.center)
        pygame.draw.rect(self.screen, (0,0,0), self.image_rect)

class Ring:
    def __init__(self,screen,value, tower):
        self.screen = screen
        self.tower = tower
        self.value = value
    
    def update(self):
        pass

