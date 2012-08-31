'''
Created on Aug 20, 2012

@author: Jami
'''
VERSION = "0.2.2"

MIN_WINDOW_WIDTH = 1024
MIN_WINDOW_HEIGHT = 768

SPLASH_TIME = 2000
STATE_LOSE_FOCUS = 2
STATE_GAIN_FOCUS = 6

COLOR_ORANGE = (250, 100, 0)
COLOR_RED = (250, 0, 0)
COLOR_GREEN = (0, 250, 0)
COLOR_BLUE = (0, 0, 250)

colors = {'orange': COLOR_ORANGE, 'red': COLOR_RED, 'green': COLOR_GREEN, 'blue': COLOR_BLUE}

PARALLAX = 1.0 # set to less than 1 for parallax

FRAMERATE = 30 # frames per second for drawing
GAMESPEED = 30 # frames per second for the game to run