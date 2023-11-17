# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 
import random
# game settings 
WIDTH = 1440
HEIGHT = 900
FPS = 30

# player settings
HP = 10
#Creates random ending location of trophey
RANDO_END = random.randint(0, WIDTH)
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
DASHING_POWER = 30
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255,255,153)
PUKEGREEN = (67,113,76)


PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 (222, 200, 100, 20, "normal"),
                 (RANDO_END, 100, 50, 20, "normal")]