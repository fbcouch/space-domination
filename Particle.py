'''
Created on Jul 7, 2012

@author: Jami
'''
from PhysicsEntity import PhysicsEntity
import pygame

class Particle(PhysicsEntity):
    '''
    class Particle
    
    '''
    spriteList = None
    currentSprite = 0
    interval = 0
    counts = 0
    
    onRemove = None
    
    target = None

    def __init__(self, spriteList = None, interval = 1, onRemove = None, target = None):
        '''
        Constructor
        '''
        super(Particle, self).__init__()
        self.spriteList = spriteList
        self.interval = interval
        self.onRemove = onRemove
        self.target = target
        
    
    def update(self, context):
        
        
        self.counts += 1
        if self.counts >= self.interval:
            self.currentSprite += 1
            if self.currentSprite < len(self.spriteList): # still more images, continue looping
                self.image = self.spriteList[self.currentSprite]
                self.rect = self.spriteList[self.currentSprite].get_rect()
            else: # no more images, call on-remove and remove self
                if self.onRemove != None: self.onRemove(context)
                self.remove(context)
                
        if self.target != None and self.rect != None:
            self.rect.left = self.target.rect.left + self.target.rect.width * 0.5 - self.rect.width * 0.5
            self.rect.top = self.target.rect.top + self.target.rect.height * 0.5 - self.rect.height * 0.5
            
    def remove(self, context):
        if(context):
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
                
                
                