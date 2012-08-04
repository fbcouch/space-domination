'''
Created on Jun 24, 2012

@author: Jami
'''

from Vec2 import Vec2
import math
import pygame

class PhysicsEntity(pygame.sprite.Sprite):
    velocity = (0,0)    # current velocity of the entity
    max_vel_sq = 1024      # maximum velocity squared (for speed)
    
    accel = (0,0)       # current acceleration
    max_accel_sq = 4    # max accel squared
    
    mass = 0            # TODO implement momentum in collisions
    
    rotation = 0        # important for acceleration stuff
    
    removeSelf = False
    
    def __init__(self):
        super(PhysicsEntity, self).__init__() # for now, we just call the super constructor
        self.original = None
        
    def accelerate(self, mag = 0):
        self.accelerate_r(mag, self.rotation)
        
    def accelerate_r(self, mag = 0, r = 0):
        # basically, we add the vector (mag, rotation) to the current accel value
        
        jerk = Vec2(mag, r)
        accel = Vec2(0,0)
        accel.setXY(self.accel[0], self.accel[1])
        
        new_accel = accel.add(jerk)
        
        if new_accel.magnitude * new_accel.magnitude <= self.max_accel_sq:
            new_accel.magnitude = math.sqrt(self.max_accel_sq)
        
        self.accel = accel.getXY()
       
       
       
    def brake(self, brake = 0):
        # to brake, we are going to subtract mag from the velocity vector until it becomes 0
        mag = math.sqrt(self.get_vel_sq())
        if mag == 0: return
        vec = Vec2(mag, math.degrees(math.asin(self.velocity[1] / mag)))
        vec.setXY(self.velocity[0],self.velocity[1])
        vec.magnitude -= brake
        if vec.magnitude < 0:
            self.velocity = (0,0)
        else:
            self.velocity = vec.getXY()
        
    def set_rotation(self, r=0):
        self.image = pygame.transform.rotate(self.original, r)
        self.rotation = r
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def get_rotation(self):
        return self.rotation
    
    def get_vel_sq(self): return (self.velocity[0] * self.velocity[0]) + (self.velocity[1] * self.velocity[1])
    
    def get_accel_sq(self): return (self.accel[0] * self.accel[0]) + (self.accel[1] * self.accel[1])
    
    '''
    ' update(context)
    ' @param context is the main game manager that exposes variables that may be needed by the update function
    '''
    def update(self, context = None):
        pass
    
    def remove(self):
        pass
    
    def collide(self, physicsEntity = None, context = None):
        pass