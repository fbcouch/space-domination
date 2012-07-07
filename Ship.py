'''
Created on May 10, 2012

@author: Jami
'''


from Bullet import Bullet
from PhysicsEntity import PhysicsEntity
from Vec2 import Vec2
from Weapon import Weapon
from pygame.locals import *
import Utils
import math
import os
import pygame
import random
import sys

class PShip(object): # Prototype for a "Ship" - IE: used in the shiplist and an actual ship can be constructed from it
    id = 0
    name = "<Undefined>"
    file = "1st_pixel_spaceship.png"
    health = 100
    hregen = 2
    shields = 100
    sregen = 2
    speed = 10
    turn = 1
    armor = 0
    
    weapons = [] # TODO

class Ship(PhysicsEntity):
    id = 0
    name = "<Undefined>"
    file = "1st_pixel_spaceship.png"
    health = 100
    hregen = 2
    shields = 100
    sregen = 2
    speed = 10
    turn = 1
    armor = 0
    max_health = 0
    max_shields = 0
    
    
    weapons = None # TODO
    selected_weapon = 0
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None):
        super(Ship, self).__init__()
        self.weapons = []
        self.constructFromProto(proto)
        self.image, self.rect = Utils.load_image(self.file)
        self.original = self.image
        self.set_position(x,y)
        self.set_rotation(r)
        
        if not parent is None: parent.add(self)
        
    def constructFromProto(self, proto = PShip()):
        if proto is None: return
        self.id = proto.id
        self.name = proto.name
        self.file = proto.file
        self.health = proto.health
        self.hregen = proto.hregen
        self.shields = proto.shields
        self.sregen = proto.sregen
        self.speed = proto.speed
        self.max_vel_sq = self.speed * self.speed
        self.max_accel_sq = self.max_vel_sq * 0.25
        self.turn = proto.turn
        self.armor = proto.armor
        self.max_health = self.health
        self.max_shields = self.shields
        
        #TODO implement loading weapons
        tempWeapon = Weapon()
        tempWeapon.max_ammo = 100
        tempWeapon.cur_ammo = 100
        tempWeapon.ammo_regen = 10
        tempWeapon.fire_rate = 100
        tempWeapon.last_fire = 0
        tempWeapon.base_damage = 5
        tempWeapon.image = "laser_yellow_sm.png"
        self.weapons.append(tempWeapon)
        
        
    '''
    fire_weapon(self, time): fires the currently selected weapon, if possible
    '''    
    def fire_weapon(self, time):
        if(self.selected_weapon < len(self.weapons) and self.weapons[self.selected_weapon].can_fire(time)):
            
            # TODO fire the weapon
            bullet = Bullet()
            bullet.image, bullet.rect = Utils.load_image(self.weapons[self.selected_weapon].image, (255,255,255))
            bullet.parent = self
            
            # move the bullet to the center-front of the ship # TODO set up custom weapon firing points
            bullet.rect.center = self.rect.left + self.rect.width * 0.5, self.rect.top + self.rect.height * 0.5
            offset = Vec2(self.rect.height * 0.5 + 10, self.get_rotation())
            offset = offset.getXY()
            bullet.rect.topleft = bullet.rect.left + offset[0], bullet.rect.top + offset[1]
            bullet.original = bullet.image
            bullet.set_rotation(self.get_rotation())
            
            # match the bullet and ship velocities TODO fixme
            vel1 = Vec2(self.weapons[self.selected_weapon].bullet_speed, self.get_rotation())
            #vel2 = Vec2(0,0)
            #vel2.setXY(self.velocity[0], self.velocity[1])
            #vel1 = vel1.add(vel2)
            bullet.velocity = vel1.getXY()
            
            # increment weapon stuff
            self.weapons[self.selected_weapon].cur_ammo -= 1
            self.weapons[self.selected_weapon].last_fire = time
            
            # set up the bullet lifetime info
            bullet.ticks_remaining = self.weapons[self.selected_weapon].bullet_ticks
            bullet.damage = self.weapons[self.selected_weapon].base_damage
            return bullet         # return the bullet
        return None
    
    def set_position(self, x, y):
        self.rect.topleft = x, y
        
    def get_position(self):
        return (self.rect.left, self.rect.top)
   
    def update(self, context = None):
        super(Ship, self).update(context)
        
        if self.removeSelf or self.health <= 0: # TODO implement explosions
            self.remove(context)
        
    def remove(self, context = None):
        if context:
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.shipSpriteGroup: context.shipSpriteGroup.remove(self)
            
    def collide(self, physicsEntity = None, context = None):
        if physicsEntity: # decrement shields and health here
            if isinstance(physicsEntity, Bullet): # a bullet hit the ship
                self.take_damage(physicsEntity.damage)
            
            else: # something else hit the ship
                self.take_damage(self.max_health / 10)
                
                    
    def take_damage(self, damage = 0):
        self.shields -= damage
        if(self.shields < 0):
            self.health += self.shields
            self.shields = 0
        
        #print "taking damage: " + str(damage) + ", health/shields: " + str(self.health) + "/" + str(self.shields)

        
    