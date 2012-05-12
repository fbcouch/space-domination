'''
Created on May 11, 2012

@author: Jami
'''

import pygame, sys, os, random, math
from pygame.locals import *
import Utils

class PhysicsEntity(pygame.sprite.Sprite):
    velocity = (0,0)    # current velocity of the entity
    max_vel_sq = 1024      # maximum velocity squared (for speed)
    
    accel = (0,0)       # current acceleration
    max_accel_sq = 4    # max accel squared
    accel_damping = 1
    
    mass = 0            # TODO implement momentum in collisions
    
    rotation = 0        # important for acceleration stuff
    
    def __init__(self):
        super(PhysicsEntity, self).__init__() # for now, we just call the super constructor
        
        
    def accelerate(self, mag = 0):
        self.accelerate_r(mag, self.rotation)
        
    def accelerate_r(self, mag = 0, r = 0):
        # basically, we add the vector (mag, rotation) to the current accel value
        if self.get_accel_sq() <= self.max_accel_sq:
            self.accel = self.accel[0] + math.cos(math.radians(r)) * mag, self.accel[1] + math.sin(math.radians(r)) * mag * -1
        if self.get_accel_sq() > self.max_accel_sq:
            if self.accel[0] == 0: 
                angle = 0
            else:
                angle = math.atan(self.accel[1] / self.accel[0])
            self.accel = math.cos(angle) * math.sqrt(self.max_accel_sq), math.sin(angle) * math.sqrt(self.max_accel_sq)       
        
    def set_rotation(self, r=0):
        self.image = pygame.transform.rotate(self.original, r)
        self.rotation = r
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def get_rotation(self):
        return self.rotation
    
    def get_vel_sq(self): return (self.velocity[0] * self.velocity[0]) + (self.velocity[1] * self.velocity[1])
    
    def get_accel_sq(self): return (self.accel[0] * self.accel[0]) + (self.accel[1] * self.accel[1])

class Physics(object):
    '''
    This class will handle all physics calculations - keeping track of movement, collision detection, etc
    '''
    
    physicsChildren = []
    
    def __init__(self):
        
        return
    
    
    def updatePhysics(self):
        for pChild in self.physicsChildren:
            # update acceleration (damping)
            if pChild.get_accel_sq() > 0:
                mag = math.sqrt(pChild.get_accel_sq())
                if mag > 0.5: mag = 0.5
                mag *= -1
                if(pChild.accel[0] == 0): angle = math.asin(pChild.accel[1] / math.fabs(pChild.accel[0]))
                else: 
                    angle = math.degrees(math.atan(pChild.accel[1] / pChild.accel[0])) + (pChild.accel[0] / math.fabs(pChild.accel[0]) - 1) * 90
                pChild.accelerate_r(mag, math.degrees(angle))
                #b
            '''if pChild.accel[0] == 0: 
                angle = 0
            else:
                angle = math.atan(pChild.accel[1] / pChild.accel[0])
            mag = (math.sqrt(pChild.get_accel_sq()) - pChild.accel_damping)
            if mag < 0: mag = 0
            pChild.accel = math.cos(angle) * mag, math.sin(angle) * mag * -1'''
            
            # update velocity
            if pChild.get_vel_sq() < pChild.max_vel_sq:
                pChild.velocity = pChild.velocity[0] + pChild.accel[0], pChild.velocity[1] + pChild.accel[1]
            if pChild.get_vel_sq() > pChild.max_vel_sq:
                # moving too fast, calculate the angle then produce a new velocity vector
                if pChild.velocity[0] == 0:
                    angle = 0
                else:
                    angle = math.atan(pChild.velocity[1] / pChild.velocity[0])
                pChild.velocity = math.cos(angle) * math.sqrt(pChild.max_vel_sq), math.sin(angle) * math.sqrt(pChild.max_vel_sq)
            
            pChild.rect.topleft = pChild.rect.left + pChild.velocity[0], pChild.rect.top + pChild.velocity[1]
            
            # TODO collision detection
            
        return
    
    
    def getChildren(self):
        return self.physicsChildren
    
    def addChild(self, pentity):
        if not pentity is None:
            self.physicsChildren.append(pentity)
            
