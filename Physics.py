'''
Created on May 11, 2012

@author: Jami
'''

import pygame, sys, os, random, math
from pygame.locals import *
import Utils


class Vec2(object):
    magnitude = 0
    theta = 0
    
    def __init__(self, mag, t):
        self.magnitude = mag
        self.theta = t
    
    def add(self, pVec = None):
        if pVec is None or not pVec is Vec2: return self
        
        v1 = self.getXY()
        v2 = pVec.getXY()
        
        v3 = v1[0] + v2[0], v1[1] + v1[1]
        self.magnitude = math.sqrt(v3[0]*v3[0] + v3[1]*v3[1])
        if not self.magnitude == 0:
            self.theta = math.degrees(math.asin(v3[1] / self.magnitude))
        else: self.theta = 0
        
        return self
        
    def getXY(self):
        return (self.magnitude * math.cos(math.radians(self.theta))), (-1 * self.magnitude * math.sin(math.radians(self.theta)))
    
    def setXY(self, x = 0.0, y = 0.0):
        mag = 0.0
        t = 0.0
        
        mag = math.sqrt(x*x + y*y)
        if mag == 0:
            self.magnitude = 0
            self.theta = 0
            return self
        
        if y == 0:
            t = math.degrees(math.acos(float(x) / float(mag)))
        elif x == 0:
            t = math.degrees(math.asin(float(- y) / float(mag)))
            
        else:
            t = math.degrees(math.atan(float(- y) / float(x)))
            if x < 0:
                t += 180
            
        self.magnitude = mag
        self.theta = (t + 360) % 360
        return self
    

class PhysicsEntity(pygame.sprite.Sprite):
    velocity = (0,0)    # current velocity of the entity
    max_vel_sq = 1024      # maximum velocity squared (for speed)
    
    accel = (0,0)       # current acceleration
    max_accel_sq = 4    # max accel squared
    
    mass = 0            # TODO implement momentum in collisions
    
    rotation = 0        # important for acceleration stuff
    
    def __init__(self):
        super(PhysicsEntity, self).__init__() # for now, we just call the super constructor
        
        
    def accelerate(self, mag = 0):
        self.accelerate_r(mag, self.rotation)
        
    def accelerate_r(self, mag = 0, r = 0):
        # basically, we add the vector (mag, rotation) to the current accel value
        
        if self.get_accel_sq() <= self.max_accel_sq:
            
            rvec = Vec2(mag, r)
            xy = rvec.getXY()
            self.accel = self.accel[0] + xy[0], self.accel[1] + xy[1] * -1
       
       
       
    def brake(self, brake = 0):
        # to brake, we are going to subtract mag from the velocity vector until it becomes 0
        print "brake"
        mag = math.sqrt(self.get_vel_sq())
        if mag == 0: return
        vec = Vec2(mag, math.degrees(math.asin(self.velocity[1] / mag)))
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

class Physics(object):
    '''
    This class will handle all physics calculations - keeping track of movement, collision detection, etc
    '''
    
    physicsChildren = []
    
    def __init__(self):
        
        return
    
    
    def updatePhysics(self):
        for pChild in self.physicsChildren:
            # accelerate
            #print "pChild-vel: " + str(pChild.velocity) + ", accel: " + str(pChild.accel)
            newVelocity = pChild.velocity[0] + pChild.accel[0], pChild.velocity[1] + pChild.accel[1]
            #print "newvelocity " + str(newVelocity) + ", max " + str(math.sqrt(pChild.max_vel_sq))
            pChild.velocity = newVelocity
            # get the velocity in the current direction of movement
            if pChild.get_vel_sq() > 0:
                vel = Vec2(0,0)
                vel.setXY(pChild.velocity[0], pChild.velocity[1])
            
                vel.theta = pChild.rotation
                
                if vel.magnitude*vel.magnitude > pChild.max_vel_sq:
                    vel.magnitude = math.sqrt(pChild.max_vel_sq)
                    pChild.velocity = vel.getXY()
            
            
            pChild.rect.topleft = pChild.rect.left + pChild.velocity[0], pChild.rect.top + pChild.velocity[1]
            
            # TODO collision detection
            
        return
    
    
    def getChildren(self):
        return self.physicsChildren
    
    def addChild(self, pentity):
        if not pentity is None:
            self.physicsChildren.append(pentity)
            
    # i need to get vec2 working properly, so I'm going to write a method to test it.
    def testVec2(self):
        '''
                            90 deg
                            
                            -y
                            |
        Coordinate system:  0,0 -> +x   --> 0 deg
                            |
                            +y
                            
                            -90 deg
        
        So, if we define a vector as (magnitude, angle) we need to remember to reverse the sign of the y axis before doing sin/asin
        from (m,a) to (x,y):
        x = m * cos(t)
        y = -1 * m * sin(t)
        
        from (x,y) to (m,a)
        m = sqrt(x*x + y*y)
        t = acos(x / m) or t = asin(-y / m)
        
        '''
        
        # test (m,a) to (x,y):
        tv = Vec2(1,0)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,45)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,90)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,135)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,180)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,225)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,270)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        tv = Vec2(1,315)
        xy = tv.getXY()
        print "Test (m,a) to (x,y): (" + str(tv.magnitude) + "," + str(tv.theta) + ") --> (" + str(xy[0]) + "," + str(xy[1]) + ")" 
        
        
        # test (x,y) to (m,a)
       
        
        xy = (1,0)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (1,-1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (0,-1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (-1,-1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (-1,0)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (-1,1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (0,1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        
        xy = (1,1)
        tv = Vec2(0,0).setXY(xy[0], xy[1])
        print "Test (x,y) to (m,a): (" + str(xy[0]) + "," + str(xy[1]) + ") --> (" + str(tv.magnitude) + "," + str(tv.theta) + ")" 
        return
            
