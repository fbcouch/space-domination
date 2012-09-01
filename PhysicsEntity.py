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
    position = (0.0, 0.0) # important for floating point physics
    
    removeSelf = False
    
    parent = None
    
    engine_points = None
    engine_color = None
    
    def __init__(self):
        super(PhysicsEntity, self).__init__() # for now, we just call the super constructor
        self.image = None
        self.rect = None
        self.original = None
        
        
        
    def accelerate(self, mag = 0):
        self.accelerate_r(mag, self.rotation)
        
    def accelerate_r(self, mag = 0, r = 0):
        # basically, we add the vector (mag, rotation) to the current accel value
        jerk = Vec2(mag, r)
        accel = Vec2(0,0)
        accel.setXY(self.accel[0], self.accel[1])
        
        new_accel = accel.add(jerk)
        if new_accel.magnitude * new_accel.magnitude > self.max_accel_sq:
            new_accel.magnitude = math.sqrt(self.max_accel_sq)
        self.accel = new_accel.getXY()
        
       
       
    def brake(self, brake = 0):
        # to brake, we are going to subtract mag from the velocity vector until it becomes 0
        mag = math.sqrt(self.get_vel_sq())
        if mag == 0: return
        vec = Vec2(0,0)#Vec2(mag, math.degrees(math.asin(self.velocity[1] / mag)))
        vec.setXY(self.velocity[0],self.velocity[1])
        vec.magnitude -= brake
        if vec.magnitude < 0:
            self.velocity = (0,0)
        else:
            self.velocity = vec.getXY()
            
        
        
    def set_rotation(self, r=0):
        self.rotation = float(r) % 360.0
        self.image = pygame.transform.rotate(self.original, int(r))
        cp = self.rect.copy()
        self.rect = self.image.get_rect(center = self.rect.center)
        self.position = (self.position[0] - cp.left + self.rect.left, self.position[1] - cp.top + self.rect.top)
        
    def get_rotation(self):
        return self.rotation
    
    def get_vel_sq(self): return (self.velocity[0] * self.velocity[0]) + (self.velocity[1] * self.velocity[1])
    
    def get_accel_sq(self): return (self.accel[0] * self.accel[0]) + (self.accel[1] * self.accel[1])
    
    '''
    ' update(context)
    ' @param context is the main game manager that exposes variables that may be needed by the update function
    '''
    def update(self, context = None, timestep = 1):
        self.rect.topleft = self.position
        
    
    def remove(self):
        pass
    
    def collide(self, physicsEntity = None, context = None):
        pass
    
    def can_collide(self, physicsEntity):
        return not self is physicsEntity.parent
    
    def will_collide(self, physicsEntity, ticks):
        '''determine if this entity will collide with physicsEntity within the given number of ticks'''
        
        # determine if we may collide
        n = 0
        test_rect_self = self.rect.copy()
        test_rect_other = physicsEntity.rect.copy()
        while n <= ticks:
            
            if test_rect_self.colliderect(test_rect_other):
                self_rect_save = self.rect.copy()
                self.rect = test_rect_self
                other_rect_save = physicsEntity.rect.copy()
                physicsEntity.rect = test_rect_other
                
                if not self.image or not physicsEntity.image:
                    collide = True
                else:
                    collide = pygame.sprite.collide_mask(self, physicsEntity)
                
                self.rect = self_rect_save
                physicsEntity.rect = other_rect_save
                
                if collide:
                    return True
            
            test_rect_self.left += self.velocity[0]
            test_rect_self.top += self.velocity[1]
            
            test_rect_other.left += physicsEntity.velocity[0]
            test_rect_other.top += physicsEntity.velocity[1]
            n += 1