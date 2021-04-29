import pygame as pg
from chaser.config import *
from chaser import brain

import random
import numpy as np

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, color=GREEN, can_move=True, is_free=False, brain=None):

        if is_free:
            self.brain = None
        else:
            self.brain = brain
            #self.brain = brain.Brain()

        self.can_move = can_move
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def decision(self, X_inputs, Y_target):
        if self.can_move==True:
            if self.brain == None:
                d = random.randint(0, 3)

            else:
                d = self.brain.get_decision(X_inputs,Y_target)
                #print("Chaser1 Decided to go : ", d)
                #self.brain.update_weights()

            direction = {0: 'W', 1: 'D', 2: 'S', 3: 'A'}
            return direction[d]
        else:
            return None

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE