'''
Created on May 10, 2012

@author: Jami
'''

from panda3d.core import TextNode, Point2, Point3, Vec3, Vec4
from Sprite import *
import Utils

class PShip: # Prototype for a "Ship" - IE: used in the shiplist and an actual ship can be constructed from it
    id = 0
    name = "<Undefined>"
    file = "gfx/1st_pixel_spaceship.png"
    health = 100
    hregen = 2
    shields = 100
    sregen = 2
    speed = 4
    turn = 5
    armor = 0
    
    weapons = [] # TODO

class Ship(Sprite):
    id = 0
    name = "<Undefined>"
    file = "gfx/1st_pixel_spaceship.png"
    health = 100
    hregen = 2
    shields = 100
    sregen = 2
    speed = 4
    turn = 5
    armor = 0
    
    weapons = [] # TODO
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None):
        super(Ship, self).__init__(Utils.loadObject(tex = proto.file, pos = Point2(x,y), parent = parent), r)
        self.constructFromProto(proto)
        
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