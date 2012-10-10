'''
Created on Jun 24, 2012

@author: Jami
'''

from Vec2 import Vec2
import consts
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
    future_positions = None # will be used for collision prediction
    rdc_rect = None # will be used for collision detection/prediction
    
    
    removeSelf = False
    
    parent = None
    
    engine_points = None
    engine_color = None
    
    target = None
    collider = None
    
    active = True
    
    
    def __init__(self):
        super(PhysicsEntity, self).__init__() # for now, we just call the super constructor
        self.image = None
        self.rect = None
        self.original = None
        
        self.rdc_rect = pygame.rect.Rect(0,0,0,0)
        
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
        
        self.predict_positions(consts.COLLIDE_TICKS, consts.COLLIDE_INTERVAL)
        predict = self.future_positions[len(self.future_positions) - 1]
        if self.rect.left < predict.left:
            self.rdc_rect.left = self.rect.left
        else:
            self.rdc_rect.left = predict.left
        
        if self.rect.right > predict.right:
            self.rdc_rect.width = self.rect.right - self.rdc_rect.left
        else:
            self.rdc_rect.width = predict.right - self.rdc_rect.left
        
        if self.rect.top < predict.top:
            self.rdc_rect.top = self.rect.top
        else:
            self.rdc_rect.top = predict.top
            
        if self.rect.bottom > predict.bottom:
            self.rdc_rect.height = self.rect.bottom - self.rdc_rect.top
        else:
            self.rdc_rect.height = predict.bottom - self.rdc_rect.top
        
        if not self.active:
            return
        
    def distance_to_sq(self, targetRect = None):
        if targetRect:
            dx = self.rect.center[0] - targetRect.center[0]
            dy = self.rect.center[1] - targetRect.center[1]
            return dx*dx + dy*dy
        return -1
    
    def consider_target(self, target):
        pass
    
    def remove(self):
        pass
    
    def collide(self, physicsEntity = None, context = None):
        pass
    
    def can_collide(self, physicsEntity):
        return not self is physicsEntity.parent
    
    def will_collide(self, physicsEntity):
        '''determine if this entity will collide with physicsEntity within the given number of ticks'''
        
        if not self.future_positions or not physicsEntity.future_positions:
            return False
        
        # determine if we may collide
        for i in range(0, len(self.future_positions)):
            if i >= len(physicsEntity.future_positions):
                return False
            
            if self.future_positions[i].colliderect(physicsEntity.future_positions[i]):
                return True
            
        return False
            
    def predict_positions(self, ticks = consts.COLLIDE_TICKS, interval = consts.COLLIDE_INTERVAL):
        '''predict the future positions of this entity'''
        n = 0
        self.future_positions = []
        n_rect = self.rect.copy()
        while n <= ticks:
            n_rect.left += self.velocity[0]
            n_rect.top += self.velocity[1]
            
            self.future_positions.append(n_rect.copy())
            
            n += interval
        