# Luis Combariza  - November 2 / 2020
# Calgary, AB

######################################################################
###################### AI LEANRS TO GAME #############################
######################################################################

# The following game and AI implementation was created as a way to
# to look into the possibilities that a simple neuro network has on
# something so difficult to a human player yet so simple to an algorithm

import pygame
import neat
import time
import os
import random

## Size of the windows used as game
WIN_WIDTH = 600
WIN_HEIGHT = 800

## importing game graphics to be used
BIRD_IMGS = [pygame.transform.scale2x(pygame.image(os.path.join("bird1.png"))),pygame.transform.scale2x(pygame.image(os.path.join("bird2.png"))),
            pygame.transform.scale2x(pygame.image(os.path.join("bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("bg.png")))


## bird class for the bird object
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.val = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # movement logic of the game objectc
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            # Absolute velocity of object falling down
            d = d/abs(d)* 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > - 90:
                self.tilt -= self.ROT_VEL


    def draw(self,win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        

