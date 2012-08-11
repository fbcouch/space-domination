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
        if self.spriteList and len(self.spriteList) > 0:
            self.image = self.spriteList[0]
            self.original = self.image
            self.rect = self.spriteList[0].get_rect()
        else:
            self.image = None
            self.rect = pygame.rect.Rect(0,0,0,0)
        
    
    def update(self, context):
        
        
        self.counts += 1
        if self.counts >= self.interval:
            self.currentSprite += 1
            if self.currentSprite < len(self.spriteList): # still more images, continue looping
                self.image = self.spriteList[self.currentSprite]
                self.original = self.image
                self.set_rotation(self.rotation)
                #self.rect = self.spriteList[self.currentSprite].get_rect()
            else: # no more images, call on-remove and remove self
                self.remove(context)
            
            self.counts = 0
            
        if self.target != None and self.rect != None:
            # TODO I seriously doubt this works...need to edit this so it works and add it to a separate function
            self.rect.left = self.target.rect.left + self.target.rect.width * 0.5 - self.rect.width * 0.5
            self.rect.top = self.target.rect.top + self.target.rect.height * 0.5 - self.rect.height * 0.5
            
    def remove(self, context):
        if self.onRemove: self.onRemove(context)
        if(context):
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
class GlowParticle(Particle):
    '''a sublcass of Particle that renders a glowing trail such as for engine glow'''
    POSSIBLE_SHAPES = ('circle', 'rect')
    
    shape = "" # possible values: circle, rect
    size = None # radius of circle or height/width of rect
    color = None # tuple containing RGB color values 0-255
    alpha = 255 # 0-255
    step = 1 # amount to decrease alpha by every interval
    
    def __init__(self, shape, size, color, alpha = 250, step = 10, interval = 1, onRemove = None, target = None):
        '''initialize the GlowParticle'''
        super(GlowParticle, self).__init__(None, interval, onRemove, target)
        if shape in self.POSSIBLE_SHAPES:
            self.shape = shape
        else:
            self.shape = self.POSSIBLE_SHAPES[0]
        
        self.size = size
        self.color = color
        self.alpha = alpha
        self.step = step
        
        # set up the image
        self.spriteList = pygame.surface.Surface((self.size, self.size))
        self.spriteList = self.spriteList.convert()
        self.spriteList.set_colorkey((0,0,0))
        # draw a shape
        if self.shape == 'circle':
            pygame.gfxdraw.filled_circle(self.spriteList, int(self.size * 0.5), int(self.size * 0.5), int(self.size * 0.5), self.color)
        elif self.shape == 'rect':
            pygame.gfxdraw.box(self.spriteList, pygame.rect.Rect(0, 0, self.size, self.size), self.color)
        self.spriteList.set_alpha(self.alpha)
        self.original = self.spriteList
        self.image = self.spriteList
        self.rect = self.spriteList.get_rect()
        self.set_rotation(self.rotation)
        
    def update(self, context):
        self.counts += 1
        if self.counts >= self.interval:
            # subtract step from alpha and apply it to the surface
            self.alpha -= self.step
            self.image.set_alpha(self.alpha)
            
            if self.alpha <= 0:
                self.remove(context)
            
            # reset the counts
            self.counts = 0
        
        if self.target and self.rect:
            # work on this
            pass
        