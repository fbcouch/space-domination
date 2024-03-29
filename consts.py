'''
Created on Aug 20, 2012

@author: Jami
'''
VERSION = "0.3.1"

MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 500

DEFAULT_WINDOW_WIDTH = 1024
DEFAULT_WINDOW_HEIGHT = 768

SPLASH_TIME = 2000
STATE_LOSE_FOCUS = 2
STATE_GAIN_FOCUS = 6

COLOR_ORANGE = (250, 100, 0)
COLOR_RED = (250, 0, 0)
COLOR_GREEN = (0, 250, 0)
COLOR_BLUE = (0, 0, 250)
COLOR_YELLOW = (250, 250, 0)

colors = {'orange': COLOR_ORANGE, 'red': COLOR_RED, 'green': COLOR_GREEN, 'blue': COLOR_BLUE}

PARALLAX = 1.0 # set to less than 1 for parallax

FRAMERATE = 60 # frames per second for drawing
GAMESPEED = 20 # frames per second for the game to run

COLLIDE_TICKS = 500
COLLIDE_INTERVAL = 10

TIME_HRS_MUL = 60*60*1000
TIME_MIN_MUL = 60*1000
TIME_SEC_MUL = 1000

PLANETS_PER_FLEET = 8