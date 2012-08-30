'''
Created on May 11, 2012

@author: Jami
'''

from Bullet import Bullet
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
    
    physicsChildren = None
    
    def __init__(self):
        self.physicsChildren = []
        
    
    
    def updatePhysics(self, context = None):
        t1 = pygame.time.get_ticks()
        i=0
        while i < len(self.physicsChildren):
            pChild = self.physicsChildren[i]                      
            
            # accelerate
            newVelocity = pChild.velocity[0] + pChild.accel[0], pChild.velocity[1] + pChild.accel[1]
            
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
            
            # Collision Detection:
            j = i + 1
            while j < len(self.physicsChildren): # check from the current sprite to the end of the list
                pCollide = self.physicsChildren[j]
                # test if these two collide by rect:
                if pygame.sprite.collide_rect(pChild,pCollide):
                    # the rectangles overlap, therefore check if colored pixels overlap:
                    if pygame.sprite.collide_mask(pChild,pCollide):
                        # this is a real collision
                        
                        if pChild.can_collide(pCollide) and pCollide.can_collide(pChild):
                            pChild.collide(pCollide, context)
                            pCollide.collide(pChild, context)
                        
                j+=1
                    
            i+=1
        
        '''# testing RDC
        collision_groups = self.collisionDetection(self.physicsChildren, 10)
        for gp in collision_groups:
            i = 0
            for i in range(0, len(gp['members'])):
                pChild = gp['members'][i]
                for j in range(i+1, len(gp['members'])):
                    pCollide = gp['members'][j]
                    if pygame.sprite.collide_rect(pChild, pCollide):
                        # the two rects collide
                        if pygame.sprite.collide_mask(pChild, pCollide):
                            # this is a real collision
                            if pChild.can_collide(pCollide) and pCollide.can_collide(pChild):
                                pChild.collide(pCollide, context)
                                pCollide.collide(pChild, context)
                    j += 1
                i += 1'''
        t2 = pygame.time.get_ticks()
        print str(t2-t1) + " / " + str(len(self.physicsChildren))
        return
    
    def collisionDetection(self, collide_list, group_size):
        '''use recursive dimensional clustering to speed up collision detection (I think this is what slows us down when there are lots of bullets flying)
           collide_list is obviously a list of PhysicsEntities, group_size is the maximum number of objects a group can have before it gets brute-forced'''
        
        parents = self.subdivide(collide_list, 0, group_size)
        children = []
        for g in parents:
            children.extend(self.subdivide(g['members'], 1, group_size))
        
        parents = children
        children = []
        for g in parents:
            children.extend(self.subdivide(g['members'], 0, group_size))
        
        
        return children
        
    def subdivide(self, collide_list, axis, group_size):
        '''recursive function that stops when the current group is <= group_size'''
        if len(collide_list) <= group_size:
            return [{'members': collide_list}]
            
        
        collide_list = self.sortChildren(collide_list, axis)
        
        groups = []
        for i in range(0, len(collide_list)):
            child = collide_list[i]
            if axis == 0:
                if len(groups) == 0:
                    # no groups, start a new one!
                    groups.append({'min': child.rect.left, 'max': child.rect.left + child.rect.width, 'members': [child]})
                else:
                    foundgroup = False
                    for g in groups:
                        if (child.rect.left <= g['max'] and child.rect.left >= g['min']) or (child.rect.left + child.rect.width <= g['max'] and child.rect.left + child.rect.width >= g['min']):
                            # it goes in this group!
                            g['members'].append(child)
                            if child.rect.left < g['min']: g['min'] = child.rect.left
                            if child.rect.left + child.rect.width > g['max']: g['max'] = child.rect.left + child.rect.width
                            foundgroup = True
                    if not foundgroup:
                        groups.append({'min': child.rect.left, 'max': child.rect.left + child.rect.width, 'members': [child]})
                        
            else:
                if len(groups) == 0:
                    groups.append({'min': child.rect.top, 'max': child.rect.top + child.rect.height, 'members': [child]})
                else:
                    foundgroup = False
                    for g in groups:
                        if (child.rect.top <= g['max'] and child.rect.top >= g['min']) or (child.rect.top + child.rect.height <= g['max'] and child.rect.top + child.rect.height >= g['min']):
                            # it goes in this group!
                            g['members'].append(child)
                            if child.rect.top < g['min']: g['min'] = child.rect.top
                            if child.rect.top + child.rect.height > g['max']: g['max'] = child.rect.top + child.rect.height
                            foundgroup = True
                    if not foundgroup:
                        groups.append({'min': child.rect.top, 'max': child.rect.top + child.rect.height, 'members': [child]})
        
        if len(groups) == 1:
            return groups
        
        returnval = []
        for g in groups:
            if len(g['members']) <= group_size:
                returnval.append(g)
            else:
                returnval.extend(self.subdivide(g['members'], axis, group_size))
            
        return returnval
            
    def sortChildren(self, sort_list, axis):
        newlist = []
        for s in sort_list:
            for n in newlist:
                if axis == 0:
                    if s is not n and s.rect.left < n.rect.left:
                        newlist.insert(newlist.index(n), s)
                        break
                else:
                    if s is not n and s.rect.top < n.rect.top:
                        newlist.insert(newlist.index(n), s)
                        break
                
            if not s in newlist:
                newlist.append(s)
                
        return newlist
    
    def getChildren(self):
        return self.physicsChildren
    
    def addChild(self, pentity):
        if not pentity is None:
            self.physicsChildren.append(pentity)
            
    
    def testRDC(self):
        rectlist = []
        one = pygame.sprite.Sprite()
        one.rect = pygame.rect.Rect(0,0,20,20)
        rectlist.append(one)
        
        one = pygame.sprite.Sprite()
        one.rect = pygame.rect.Rect(10, 10, 20, 20)
        rectlist.append(one)
        
        one = pygame.sprite.Sprite()
        one.rect = pygame.rect.Rect(40, 40, 20, 20)
        rectlist.append(one)
        
        print self.collisionDetection(rectlist, 1)
    
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

if __name__ == "__main__":
    p = Physics()
    p.testRDC()
