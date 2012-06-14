'''
Created on Jun 13, 2012

@author: Jami
'''
import pygame, sys, os, random, math
from pygame.locals import *

class MenuButton(pygame.sprite.Sprite):
    # the default behavior will be to make the sprite slightly larger (scale to 1.2f) when button pressed & return to normal size on release or mouse off
    text = None
    
    
    def __init__(self):
        super(MenuButton, self).__init__()
        
    def onMouseOver(self):
        return
    
    def onMouseOff(self):
        return
    
    def onButtonPressed(self):
        
        return
    
    def onButtonReleased(self):
        
        return self.onClick()
    
    def onClick(self):
        
        return
    
class MenuManager(object):
    
    def __init__(self):
        
        return