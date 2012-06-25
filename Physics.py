'''
Created on May 11, 2012

@author: Jami
'''

from Ship import Bullet
from pygame.locals import *
import Utils
from Vec2  import Vec2
import pygame
import sys
import os
import random
import math

class Physics(object):
    '''
    This class will handle all physics calculations - keeping track of movement, collision detection, etc
    '''
    
    physicsChildren = []
    
    def __init__(self):
        
        return
    
    
    def updatePhysics(self):
        
        i=0
        while i < len(self.physicsChildren):
            pChild = self.physicsChildren[i]           
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
            j = i + 1
            while j < len(self.physicsChildren):
                pCollide = self.physicsChildren[j]
                # test if these two collide by rect:
                if not (isinstance(pChild, Bullet) and isinstance(pCollide, Bullet)):
                    if pygame.sprite.collide_rect(pChild,pCollide):
                        # the rectangles overlap
                        if pygame.sprite.collide_mask(pChild,pCollide):
                            # this is a real collision
                            # TODO check health, etc
                            pChild.removeSelf = True
                            pCollide.removeSelf = True
                            self.physicsChildren.remove(pChild)
                            self.physicsChildren.remove(pCollide)
                j+=1
                    
            i+=1
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
            
