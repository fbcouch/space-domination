'''
Created on Jul 16, 2012

@author: jami
'''
import Utils
import pygame

class PopupMessage(object):
    '''
    classdocs
    '''
    icon = None
    title = ""
    body = ""
    
    duration = 0
    
    font = None
    
    surface = None

    def __init__(self, title, body, duration, icon = None, font = None):
        '''
        Constructor
        '''
        self.title = title
        self.body = body
        self.icon = icon
        self.duration = duration
        self.font = font
        if not self.font:
            self.font = pygame.font.Font(None, 20)
            
        titleSurface = self.font.render(self.title, 1, (204, 204, 204))
        self.body = Utils.parse(body, 500, self.font)
        bodySurfaces = []
        maxWidth = titleSurface.get_width()
        for str in self.body:
            bodySurfaces.append(self.font.render(str, 1, (204, 255, 204)))
            if bodySurfaces[len(bodySurfaces) - 1].get_width() > maxWidth:
                maxWidth = bodySurfaces[len(bodySurfaces) - 1].get_width()
        
        y = 0
        textSurface = pygame.Surface((maxWidth, titleSurface.get_height() + 2 + (bodySurfaces[0].get_height() + 2) * len(bodySurfaces) ))
        textSurface.blit(titleSurface, (0,y))
        y += titleSurface.get_height() + 2
        for surf in bodySurfaces:
            textSurface.blit(surf, (0, y))
            y += surf.get_height() + 2
        
        if self.icon:
            self.surface = pygame.Surface((self.icon.get_width() + textSurface.get_width(), self.icon.get_height() + textSurface.get_height()))
            self.surface.blit(self.icon, (0,0))
            self.surface.blit(textSurface, (self.icon.get_width(),0))
        else:
            self.surface = textSurface
        
    def update(self, context = None):
        self.duration -= 1
        if context and self.duration <= 0:
            if self in context.messageList: context.messageList.remove(self)
        
    
            