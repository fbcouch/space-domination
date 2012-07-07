'''
Created on Jul 4, 2012

@author: Jami
'''
from Particle import Particle
from PhysicsEntity import PhysicsEntity
from Utils import load_sprite_sheet
import pygame


class Bullet(PhysicsEntity):
    
    parent = None
    ticks_remaining = 0
    damage = 0
    
    def __init__(self):
        super(Bullet, self).__init__()
    
    def update(self, context = None):
        super(Bullet, self).update(context)
        
        self.ticks_remaining -= 1;
        
        if (self.ticks_remaining <= 0 or self.removeSelf):
            self.remove(context)
        
    def remove(self, context = None):
        if(context):
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
    def collide(self, physicsEntity = None, context = None):
        if(physicsEntity and not isinstance(physicsEntity, Bullet)):
            
            explosion = Particle(load_sprite_sheet('explosion3.png', 100, 100, colorkey = -1), target = self)
            
            context.foregroundSpriteGroup.add(explosion)
            self.remove(context)