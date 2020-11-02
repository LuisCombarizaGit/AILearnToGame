# Luis Combariza  - November 2 / 2020


######################################################################
###################### AI LEANRS TO GAME #############################
######################################################################

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
        return


        

