#By Eli Brenckle

import pygame as pg
from pygame.sprite import Sprite
from pygame.math import Vector2 as vec
import os
from settings import *
import time
from math import *
import math

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')


class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.countdown = Cooldown()
        self.cd_boost = Cooldown()
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        self.canmove = True
        self.candash = True
        self.notdashing = True
        self.candoublejump = False
        self.canjump = True
        self.timesjumped = 0
    def controls(self):
        if self.canmove == True:
            keys = pg.key.get_pressed()
            if keys[pg.K_LSHIFT]:
                self.boost()
            if keys[pg.K_a]:
                self.acc.x = -3
            if keys[pg.K_d]:
                self.acc.x = 3
            if keys[pg.K_SPACE]:
                self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        # ghits = pg.sprite.collide_rect(self, self.game.ground)
        #checks if the ground is collided with, if it is then resets jumps
        if hits:
            self.timesjumped = 0
            self.canjump = True
        if mhits:
            self.timesjumped = 1
            self.canjump = True
        #checks to see if you can double jump, then sets limit on amount of tmes you can jump.
        if self.candoublejump:
            if self.timesjumped < 2:
                print("i can jump")
                self.vel.y = -PLAYER_JUMP
                self.timesjumped += 1
                print(self.timesjumped)
        #if double jump is false then only allow one jump
        else:
            if self.timesjumped < 1:
                print("i can jump")
                self.vel.y = -PLAYER_JUMP
                self.timesjumped += 1
                print(self.timesjumped)
    def update(self):
        self.countdown.ticking()
        self.cd_boost.ticking()
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        #if you leave the borders it teleports you back to begining
        if self.pos.y > HEIGHT or self.pos.x < 0 or self.pos.x > WIDTH:
            self.pos = vec(WIDTH/2, HEIGHT/2)
        #If you collide with a mob then rebound in the opposite direction.
        #reverses any momentum you have if colliding with bounce pad
        if pg.sprite.spritecollide(self, self.game.all_mobs, False):
            self.vel.x = -self.vel.x
            self.acc.x = -self.acc.x
            self.vel.y = -self.vel.y
            self.acc.y = -self.acc.y
            self.timesjumped = 1
        #allows player to double jump when collecting powerup
        if pg.sprite.spritecollide(self, self.game.all_upgrades, True):
            self.candoublejump = True
        #once tophey is reached end the game
        if pg.sprite.spritecollide(self, self.game.trophy, False):
            pg.quit()
        

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)

class Upgrade(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(WIDTH/2, HEIGHT/2)
    def update(self):
        pass

class Trophy(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image = pg.image.load(os.path.join(img_folder, 'trophy.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(WIDTH/2, HEIGHT/2)
    def update(self):
        pass
        
# Cooldown from Mr. Cozorts weirdGame. Not used but still here.
class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
    def ticking(self):
        self.current_time = math.floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
        # print(self.delta)
    def timer(self):
        self.current_time = math.floor((pg.time.get_ticks())/1000)
    
