'''
Created on Jul 16, 2012

@author: jami
'''
import Utils
import os
import pygame



class PopupMessage(object):
    '''
    classdocs
    '''
    DEFAULT_DURATION = 600
    
    icon = None
    title = ""
    body = ""
    
    duration = 0
    
    font = None
    
    surface = None

    def __init__(self, title, body, duration, width, icon = None, font = None):
        '''
        Constructor
        '''
        self.title = title
        self.body = body
        self.icon = icon
        self.duration = duration
        self.font = font
        if not self.font:
            self.font = pygame.font.Font(os.path.join("assets", "promethean.ttf"), 20)
            
        titleSurface = self.font.render(self.title, 1, (204, 204, 204))
        if self.icon:
            self.body = Utils.parse(body, width - self.icon.get_width(), self.font)
        else:
            self.body = Utils.parse(body, width, self.font)
        bodySurfaces = []
        maxWidth = titleSurface.get_width()
        for str in self.body:
            bodySurfaces.append(self.font.render(str, 1, (204, 255, 204)))
            if bodySurfaces[len(bodySurfaces) - 1].get_width() > maxWidth:
                maxWidth = bodySurfaces[len(bodySurfaces) - 1].get_width()
        
        y = 0
        textSurface = pygame.Surface((maxWidth, titleSurface.get_height() + 2 + (bodySurfaces[0].get_height() + 2) * len(bodySurfaces) ))
        textSurface.set_colorkey((0,0,0))
        textSurface.blit(titleSurface, (0,y))
        y += titleSurface.get_height() + 2
        for surf in bodySurfaces:
            textSurface.blit(surf, (0, y))
            y += surf.get_height() + 2
        
        if self.icon:
            self.surface = pygame.Surface((self.icon.get_width() + textSurface.get_width(), self.icon.get_height() + textSurface.get_height()))
            self.surface.set_colorkey((0,0,0))
            self.surface.blit(self.icon, (0,0))
            self.surface.blit(textSurface, (self.icon.get_width(),0))
        else:
            self.surface = textSurface
        
    def update(self, parent = None):
        self.duration -= 1
        if parent and self.duration <= 0:
            if self in parent: parent.remove(self)
        
    
            