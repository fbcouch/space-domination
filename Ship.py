'''
Created on May 10, 2012

@author: Jami
'''


from Bullet import Bullet
from Particle import Particle
from PhysicsEntity import PhysicsEntity
from Utils import load_sprite_sheet, load_image
from Vec2 import Vec2
from Weapon import Weapon
from pygame.locals import *
from xml.sax import handler, make_parser
import Utils
import math
import os
import pygame
import random
import sys
import traceback

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
    
    engine_points = None
    
    weapons = None
    
    image = None
    
    def __init__(self):
        self.weapons = []

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
    
    tag = ""
    
    
    weapons = None
    selected_weapon = 0
    
    ticks_for_regen = 30
    
    hard_points = None
    
    engine_points = None
    
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None):
        super(Ship, self).__init__()
        self.weapons = []
        self.constructFromProto(proto, context)
        self.original = self.image
        self.set_position(x,y)
        self.set_rotation(r)
        
        #if not parent is None: parent.add(self)
        self.parent = parent
        
        self.hard_points = []
        
    def constructFromProto(self, proto = PShip(), context = None):
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
        
        
        if not proto.image:
            try:
                self.image, self.rect = Utils.load_image(self.file, -1)
            except SystemExit, message:
                print message
                self.image = pygame.surface.Surface((10,10))
                pygame.gfxdraw.filled_circle(self.image, 5, 5, 5, (51, 102, 255))
                self.rect = self.image.get_rect()
        else:
            self.image = proto.image
            self.rect = self.image.get_rect()
        
        for weapon in proto.weapons:
            if context != None and weapon['id'] >= 0 and weapon['id'] < len(context.weaponList):
                self.weapons.append(context.weaponList[weapon['id']].clone())
            else:
                self.weapons.append(Weapon())
            if 'points' in weapon and weapon['points']:
                self.weapons[len(self.weapons) - 1].set_points(weapon['points'])
                
        if proto.engine_points:
            self.engine_points = Utils.parse_pointlist(proto.engine_points)
        
    '''
    fire_weapon(self, time): fires the currently selected weapon, if possible
    '''    
    def fire_weapon(self, time):
        if(self.selected_weapon < len(self.weapons) and self.weapons[self.selected_weapon].can_fire(time)):
            
            # TODO fire the weapon
            bullets = []
            weapon = self.weapons[self.selected_weapon]
            if weapon.fire_points and len(weapon.fire_points) > 0:
                for point in weapon.fire_points:
                    bullets.append(Bullet())
            else:
                bullets.append(Bullet())
            #bullet = Bullet()
            n = 0
            for bullet in bullets:
                if not weapon.image:
                    bullet.image, bullet.rect = Utils.load_image(weapon.image, (255,255,255))
                else:
                    bullet.image = weapon.image
                    bullet.rect = bullet.image.get_rect()
                    
                bullet.parent = self
                if self.parent and self in self.parent.hard_points:
                    bullet.parent = self.parent
                
                if weapon.fire_points and len(weapon.fire_points) > n:
                    # move the bullet to the specified point
                    offset = Vec2(0,0)
                    offset.setXY(weapon.fire_points[n][0] - self.original.get_rect().width * 0.5 + bullet.rect.width, weapon.fire_points[n][1] - self.original.get_rect().height * 0.5)
                    offset.theta += self.get_rotation()
                    offset = offset.getXY()
                    bullet.rect.center = self.rect.center
                    bullet.rect.topleft = bullet.rect.left + offset[0], bullet.rect.top + offset[1]
                else:
                    # move the bullet to the center-front of the ship
                    bullet.rect.center = self.rect.left + self.rect.width * 0.5, self.rect.top + self.rect.height * 0.5
                    offset = Vec2(self.rect.height * 0.5 + bullet.rect.width, self.get_rotation())
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
                
                n += 1
                
            return bullets         # return the bullet list
        return None
    
    def set_position(self, x, y):
        self.rect.topleft = x, y
        
    def get_position(self):
        return (self.rect.left, self.rect.top)
   
    def update(self, context = None):
        super(Ship, self).update(context)
        
        #for pt in self.hard_points:
        #    pt.update(context)
        
        if self.ticks_for_regen == 0:
            # health regen
            self.health += self.hregen
            if self.health > self.max_health:
                self.health = self.max_health
                
            # shield regen
            self.shields += self.sregen
            if self.shields > self.max_shields:
                self.shields = self.max_shields
                
            # ammo regen
            for wp in self.weapons:
                wp.cur_ammo += wp.ammo_regen
                if wp.cur_ammo > wp.max_ammo:
                    wp.cur_ammo = wp.max_ammo
            
            self.ticks_for_regen = 30
        else:
            self.ticks_for_regen -= 1
        
        if self.engine_points and (self.accel[0] != 0 or self.accel[1] != 0):
            for ep in self.engine_points:
                engine_glow = Particle(load_sprite_sheet('engine1_10.png', 10, 10, colorkey = -1), interval = 2)
                offset = Vec2(0,0)
                offset.setXY(ep[0] - 0.5 * self.original.get_rect().width, ep[1] - 0.5 * self.original.get_rect().height)
                offset.theta += self.rotation
                offset = offset.getXY()
                engine_glow.rect.center = (self.rect.center[0] + offset[0], self.rect.center[1] + offset[1])
                engine_glow.set_rotation(self.rotation)
                context.foregroundSpriteGroup.add(engine_glow)
        
        if self.removeSelf or self.health <= 0: # TODO implement explosions
            explosion = Particle(load_sprite_sheet('explosion1.png', 100, 100, colorkey = -1), target = self)
            context.foregroundSpriteGroup.add(explosion)
            self.remove(context)
        
    def remove(self, context = None):
        #traceback.print_stack()
        
        if context:
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.shipSpriteGroup: context.shipSpriteGroup.remove(self)
            for hp in self.hard_points:
                if hp in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(hp)
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
        
        if self.parent:
            if self in self.parent.hard_points: self.parent.hard_points.remove(self)
            
    def collide(self, physicsEntity = None, context = None):
        if physicsEntity: # decrement shields and health here
            if isinstance(physicsEntity, Bullet): # a bullet hit the ship
                self.take_damage(physicsEntity.damage)
            
            else: # something else hit the ship
                self.take_damage(10)
                
                    
    def take_damage(self, damage = 0):
        self.shields -= damage
        if(self.shields < 0):
            self.health += self.shields
            self.shields = 0
        
        #print "taking damage: " + str(damage) + ", health/shields: " + str(self.health) + "/" + str(self.shields)

        
class ShipListXMLParser(handler.ContentHandler):
    shipList = None
    ship = None
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.shipList = []
    
    def loadShipList(self, filename = "assets/shiplist.xml"):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
        return self.shipList
    
    def startElement(self, name, attrs):
        if name == "shiplist":
            self.shipList = []
        elif name == "ship":
            self.ship = PShip()
            
            self.ship.id = int(attrs.get('id'))
            self.ship.name = attrs.get('name', 'default ship')
            self.ship.health = int(attrs.get('health', 100))
            self.ship.hregen = int(attrs.get('hregen', 0))
            self.ship.shields = int(attrs.get('shields', 100))
            self.ship.sregen = int(attrs.get('sregen', 2))
            self.ship.speed = int(attrs.get('speed', 5))
            self.ship.turn = int(attrs.get('turn', 5))
            self.ship.armor = int(attrs.get('armor', 0))
            self.ship.engine_points = attrs.get('engines', '')
            
            self.ship.file = attrs.get('file','')
            
            if not(self.ship.file == None):
                try:
                    image, rect = load_image(self.ship.file, colorkey = -1)
                except SystemExit, message:
                    image = None
                    print "Error loading file: " + self.ship.file
                self.ship.image = image
            else:
                self.ship.image = None
            
            
            
            
            self.shipList.append(self.ship)
        
        elif name == "weapon":
            self.ship.weapons.append({'id':int(attrs.get('id', '0')), 'points':attrs.get('points')})
            
            
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass