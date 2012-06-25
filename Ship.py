'''
Created on May 10, 2012

@author: Jami
'''


import pygame, sys, os, random, math
from pygame.locals import *
import Utils
from PhysicsEntity import PhysicsEntity
from Vec2 import Vec2         

class PShip(object): # Prototype for a "Ship" - IE: used in the shiplist and an actual ship can be constructed from it
    id = 0
    name = "<Undefined>"
    file = "1st_pixel_spaceship.png"
    health = 100
    hregen = 2
    shields = 100
    sregen = 2
    speed = 4
    turn = 5
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
    speed = 4
    turn = 5
    armor = 0
    
    
    weapons = [] # TODO
    selected_weapon = 0
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None):
        super(Ship, self).__init__()
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
            offset = Vec2(self.rect.width * 0.5, self.get_rotation())
            offset = offset.getXY()
            bullet.rect.topleft = bullet.rect.left + offset[0], bullet.rect.top + offset[1]
            bullet.original = bullet.image
            bullet.set_rotation(self.get_rotation())
            
            # match the bullet and ship velocities
            vel1 = Vec2(self.weapons[self.selected_weapon].bullet_speed, self.get_rotation())
            vel2 = Vec2(0,0)
            vel2.setXY(self.velocity[0], self.velocity[1])
            vel1 = vel1.add(vel2)
            bullet.velocity = vel1.getXY()
            
            # increment weapon stuff
            self.weapons[self.selected_weapon].cur_ammo -= 1
            self.weapons[self.selected_weapon].last_fire = time
            
            # set up the bullet lifetime info
            bullet.ticks_remaining = self.weapons[self.selected_weapon].bullet_ticks
            return bullet         # return the bullet
        return None
    
    def set_position(self, x, y):
        self.rect.topleft = x, y
        
    def get_position(self):
        return (self.rect.left, self.rect.top)
    
class Weapon(object):
    max_ammo = 0
    cur_ammo = 0
    ammo_regen = 0
    fire_rate = 0
    last_fire = 0
    base_damage = 0
    bullet_ticks = 100
    bullet_speed = 20
    
    image = None
    
    def can_fire(self, time):
        if (self.cur_ammo > 0 and time > self.last_fire + self.fire_rate):
            return True
        return False
    
class Bullet(PhysicsEntity):
    
    parent = None
    ticks_remaining = 0
    
    def __init__(self):
        super(Bullet, self).__init__()
        
    