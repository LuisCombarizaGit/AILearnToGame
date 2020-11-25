# Luis Combariza  - November 2 / 2020
# Calgary, AB
# luis_combariza@outlook.com
# luisCombariza@linkedIn.com

######################################################################
###################### AI LEARNS TO GAME #############################
######################################################################

# The following game and AI implementation are created as a way to
# to look into the possibilities that a simple neuro network has on
# something so difficult to a human player yet so simple to an algorithm

# GAME STORY : You have landed on strange sandy planet with landscape much like our own
# country of Egypt. You are running out of fuel and to survive you must
# not crash as you make through the terrain. You set set up the autopilot(AI)
# in hope that it will save you.

import pygame
pygame.font.init()
import neat
import time
import os
import random

## Size of the windows used as game
WIN_WIDTH = 550
WIN_HEIGHT = 800

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

## importing game graphics to be used
SHIP_IMGS = [(pygame.image.load(os.path.join("ship_1.png"))),(pygame.image.load(os.path.join("ship_2.png"))),
            (pygame.image.load(os.path.join("Ship_3.png")))]
TREE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("treeLong.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))
BG_IMG = pygame.image.load(os.path.join("backgroundColorDesert.png"))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Tree class that represents the obstacles that the object will go by
class Tree():
    GAP = 200
    VEL = 5

    # Initialize the Tree object obstacles for the ship to pass by
    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.TREE_TOP = pygame.transform.flip(TREE_IMG, False, True)
        self.TREE_BOTTOM = TREE_IMG

        self.passed = False
        self.set_height()

    # Sets height of Pipe at random
    def set_height(self):
        self.height = random.randrange(50 , 450)
        self.top = self.height - self.TREE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self,win):
        win.blit(self.TREE_TOP,(self.x, self.top))
        win.blit(self.TREE_BOTTOM,(self.x, self.bottom))

    # Collision method that checks if two images ( masks ) collide
    def collide(self,ship):
        ship_mask = ship.get_mask()
        top_mask = pygame.mask.from_surface(self.TREE_TOP)
        bottom_mask = pygame.mask.from_surface(self.TREE_BOTTOM)
        
        top_offset = (self.x - ship.x, self.top - round(ship.y))
        bottom_offset = (self.x - ship.x, self.bottom - round(ship.y))

        b_point = ship_mask.overlap(bottom_mask, bottom_offset)
        t_point = ship_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

# class that represents the base of the game and how it will move
class Base():
    VEL = 2
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


# Ship class for the ship object
class Ship:
    IMGS = SHIP_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    # Initialize the game object ( ship )
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

        # movement logic of the game object
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

def draw_window(win,ship,trees,base,score):
    win.blit(BG_IMG, (0,0))

    for tree in trees:
        tree.draw(win)

    text = STAT_FONT.render("Score: "+ str(score), 1, (0,0,0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(),10))
    base.draw(win)

    ship.draw(win)
    pygame.display.update()

def main(genomes,config):

    nets = []
    ge = []
    ships = []

    for g in genomes:
        net = neat.nn.FeedForwardNetwork(g, config)
        nets.append(net)
        ships.append(Ship(100,340))
        g.fitness = 0
        ge.append(g)


    base = Base(730)
    trees = [Tree(500)]
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        rem = []
        add_tree = False
        for tree in trees:
            for ship in ships:
                if tree.collide(ship):
                    pass

                if not tree.passed and tree.x < ship.x:
                    tree.passed = True
                    add_tree = True

            if tree.x + tree.TREE_TOP.get_width() < 0:
                rem.append(tree)

            tree.move()

        if add_tree:
            score += 1
            trees.append(Tree(500))
        for r in rem:
            trees.remove(r)

        for ship in ships:
            if ship.y + ship.img.get_height() >=730:
                pass

        base.move()
        draw_window(win,ship,trees,base,score)

    pygame.quit()
    quit()

main()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stat = neat.StatisticsReporter()
    p.add_reporter(stat)

    winner = p.run(main,50)




if __name__== "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)
