# Luis Combariza  - November 2 / 2020
# Calgary, AB

######################################################################
###################### AI LEARNS TO GAME #############################
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
WIN_WIDTH = 550
WIN_HEIGHT = 800

## importing game graphics to be used
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("bg.png")))


# Pipe class that represents the obstacles that the object will go by
class Pipe:
    GAP = 200
    VEL = 5

    # Initialize the Pipe object
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    # Sets height of Pipe at random
    def set_height(self):
        self.height = random.randrange(20 , 420)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x, self.top))
        win.blit(self.PIPE_BOTTOM,(self.x, self.bottom))

    # Collision method that checks if two images ( masks ) collide
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False

# class that represents the base of the game and how it will move
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    # Movement of the base
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1,self.y))
        win.blit(self.IMG, (self.x2, self.y))


# bird class for the bird object
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    # Initialize the game object ( bird )
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # Jump method that defines how the object jumps
    def jump(self):
        self.val = -10.5
        self.tick_count = 0
        self.height = self.y

    # Move method that defines how the object will move
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

    # Draw method that defines how the object will be drawn on canvas based
    # on the actions done
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
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # Two dimensional list of the location of pixels of each image
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(win,bird,pipes,base):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(250,350)
    base = Base(740)
    pipes = [Pipe(700)]
    score = 0

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        add_pipe = False
        rem  = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(800))
        for r in rem:
            pipes.remove(r)

        base.move()
        draw_window(win,bird,pipes,base)
    pygame.quit()
    quit()


main()


