'''
Created on May 10, 2012

@author: Jami
'''


import pygame, sys, os, random
from pygame.locals import *
import Utils
from Physics import *

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
    '''
    fire_weapon(self, time): fires the currently selected weapon, if possible
    '''    
    def fire_weapon(self, time, spriteGroup = None):
        if(self.selected_weapon < len(self.weapons) and self.selected_weapon.can_fire(time)):
            # TODO fire the weapon
            return
    
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
    
    image = None
    
    def can_fire(self, time):
        if (self.cur_ammo > 0 and time > self.last_fire + self.fire_rate):
            return True
        return False