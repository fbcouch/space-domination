'''
Created on Jul 19, 2012

@author: Jami
'''
import Utils

class HUD(object):
    '''
    classdocs
    '''
    hud_bottom = None

    def __init__(self):
        '''
        Constructor
        '''
        self.hud_bottom, rect = Utils.load_image("hud_lower.png", colorkey = -1)
        
    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.hud_bottom, (0, screen.get_height() - self.hud_bottom.get_height()))