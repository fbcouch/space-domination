'''
Created on Jul 16, 2012

@author: jami
'''
from Mission import Mission, Background
import Utils
import os
import pygame

class Mission01(Mission):
    '''
    classdocs
    '''
    missionName = "Flight Training"
    missionDesc = "Your first introduction to the magical world of spaceflight"

    

    def __init__(self):
        '''
        Constructor
        '''
        super(Mission01, self).__init__()
        
        try:
            self.icon, rect = Utils.load_image(os.path.join("mission01","icon.png"), colorkey = -1)
        except SystemExit, message:
            self.icon = None
        
        bg = Background()
        bg.filename = "default_background.png"
        bg.scale = 1.0
        bg.x = 0.0
        bg.y = 0.0
        
        
    def build(self):
        pass
        
    def update(self, context = None):
        super(Mission01, self).update(context)