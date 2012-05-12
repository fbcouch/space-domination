'''
Created on May 10, 2012

@author: Jami
'''


import pygame, sys, os, random
from pygame.locals import *
import Utils

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

class Ship(pygame.sprite.Sprite):
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
    rotation = 0
    
    weapons = [] # TODO
    
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
        self.turn = proto.turn
        self.armor = proto.armor
        
        #TODO implement loading weapons
        
    def set_rotation(self, r=0):
        self.image = pygame.transform.rotate(self.original, r)
        self.rotation = r
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def get_rotation(self):
        return self.rotation
    
    def set_position(self, x, y):
        self.rect.topleft = x, y
        
    def get_position(self):
        return (self.rect.left, self.rect.top)