'''
Created on Jul 4, 2012

@author: Jami
'''
from Ship import Ship, PShip
from Vec2 import Vec2
import math
import pygame
import random

class AIShip(Ship):
    home_position = None
    waypoint = None
    area_size = 250
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None):
        super(AIShip,self).__init__(x, y, r, proto, parent, context)
        self.home_position = (x, y)
        self.waypoint = self.update_waypoint()
        
    def update(self, context = None):
        super(AIShip, self).update(context)
        
        if context and self.distance_to_sq(context.playerShip.rect) < self.area_size * self.area_size:
            # we are near the target - face & attack it!
            self.face_target(context.playerShip.rect.center)
            
            # accelerate toward target
            self.accelerate(self.speed * 0.25)
                        
            bullet = self.fire_weapon(context.timeTotal)
                
            if not (bullet is None):
                context.physics.addChild(bullet)
                context.foregroundSpriteGroup.add(bullet)
        else:
            if self.rect.collidepoint(self.waypoint):
                self.waypoint = self.update_waypoint()
            
            # we are not near the target (or didn't give a context)
            self.face_target(self.waypoint)
            
            # accelerate toward target
            self.accelerate(self.speed * 0.25)
            
            
            
    def face_target(self, target):
  
        dx = target[0] - self.rect.left
        dy = target[1] - self.rect.top
        angle = Vec2(0,0)
        angle.setXY(dx, dy)
        targetAngle = (angle.theta) % 360
        dT = targetAngle - self.get_rotation()
        if dT > 180:
            dT = dT - 360
        elif dT < -180:
            dT += 360
        
        if dT > self.turn: 
            self.set_rotation((self.get_rotation() + self.turn) % 360)
        elif dT < -1 * self.turn:
            self.set_rotation((self.get_rotation() - self.turn) % 360)
        else:
            self.set_rotation(targetAngle)
            
        return dT

    def distance_to_sq(self, targetRect = None):
        if targetRect:
            dx = self.rect.left - targetRect.left
            dy = self.rect.top - targetRect.top
            return dx*dx + dy*dy
        return -1
            
    def update_waypoint(self):
        return (self.home_position[0] + random.randint(-1 * self.area_size, self.area_size), self.home_position[1] + random.randint(-1 * self.area_size, self.area_size))
    