'''
Created on May 10, 2012

@author: Jami
'''


from Bullet import Bullet
from Particle import Particle, GlowParticle
from PhysicsEntity import PhysicsEntity
from Utils import load_sprite_sheet, load_image
from Vec2 import Vec2
from Weapon import Weapon
from pygame.locals import *
from xml.sax import handler, make_parser
import Utils
import consts
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
    team = -1
    player_flyable = False
    
    engine_points = None
    engine_color = "orange"
    
    weapons = None
    
    hard_points = None
    
    spawn = None
    
    image = None
    
    def __init__(self):
        self.weapons = []

class Upgrade(object):
    # for ship
    health = 0
    hregen = 0
    shields = 0
    sregen = 0
    speed = 0
    turn = 0
    armor = 0
    
    # for weapons
    damage = 0
    
    
    # for store
    cost = 0
    type = ""
    name = ""
    
    def __init__(self, attrs = None):
        if attrs:
            self.health = int(attrs.get('health', '0'))
            self.hregen = float(attrs.get('hregen', 0))
            self.shields = int(attrs.get('shields', 0))
            self.sregen = float(attrs.get('sregen', 0))
            self.speed = float(attrs.get('speed', 0))
            self.turn = float(attrs.get('turn', 0))
            self.armor = float(attrs.get('armor', 0))
            
            self.damage = float(attrs.get('damage', 0))
            
            self.type = attrs.get('type', 'default')
            self.name = attrs.get('name', '<Unnamed Upgrade>')
            self.cost = int(attrs.get('cost', 0))
    
    def __add__(self, other):
        self.health += other.health
        self.hregen += other.hregen
        self.shields += other.shields
        self.sregen += other.sregen
        self.speed += other.speed
        self.turn += other.turn
        self.armor += other.armor
        
        self.damage += other.damage
        
        return self
        
    def __sub__(self, other):
        self.health -= other.health
        self.hregen -= other.hregen
        self.shields -= other.shields
        self.sregen -= other.sregen
        self.speed -= other.speed
        self.turn -= other.turn
        self.armor -= other.armor
        
        self.damage -= other.damage
        
        return self

class Ship(PhysicsEntity):
    TEAM_DEFAULT_FRIENDLY = 0
    TEAM_DEFAULT_ENEMY = 1
    
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
    team = TEAM_DEFAULT_ENEMY
    
    tag = ""
    
    stats = None
    
    weapons = None
    selected_weapon = 0
    
    ticks_for_regen = 30.0
    
    hard_points = None
    
    engine_blip_time = 0.0
    
    target_box = None
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None):
        super(Ship, self).__init__()
        self.weapons = []
        self.constructFromProto(proto, context)
        self.original = self.image
        self.set_position(x,y)
        self.set_rotation(r)
        self.stats = {'kills': 0, 'shots-fired': 0, 'shots-hit': 0, 'damage-dealt': 0, 'damage-taken': 0, 'damaged-by': {}}
        
        
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
        self.team = proto.team

        
        
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
        
        if proto.engine_color and proto.engine_color in consts.colors:
            self.engine_color = consts.colors[proto.engine_color]

     
    def fire_weapon(self, time):
        '''
        fire_weapon(self, time): fires the currently selected weapon, if possible
        '''   
        if(self.selected_weapon < len(self.weapons) and self.weapons[self.selected_weapon].can_fire()):
            
            # increment the stats
            if self.parent and self in self.parent.hard_points:
                bullets = self.weapons[self.selected_weapon].fire(time, self.parent, self, self.get_rotation(), self.parent.velocity)
                self.parent.stats['shots-fired'] += len(bullets)
            else:
                bullets = self.weapons[self.selected_weapon].fire(time, self, self, self.get_rotation(), self.velocity)
                self.stats['shots-fired'] += len(bullets)
            return bullets         # return the bullet list
        return None
    
    def set_position(self, x, y):
        self.position = (x, y)
        self.rect.topleft = x, y
        
    def get_position(self):
        return self.position#(self.rect.left, self.rect.top)
   
    def update(self, context = None, timestep = 1):
        super(Ship, self).update(context, timestep)
        if not self.active:
            return
        
        #for pt in self.hard_points:
        #    pt.update(context)
        for wp in self.weapons:
            wp.update(context, timestep)
            
        
        # health regen
        self.health += self.hregen * timestep / consts.GAMESPEED
        if self.health > self.max_health:
            self.health = self.max_health
        
        # shield regen
        self.shields += self.sregen * timestep / consts.GAMESPEED
        if self.shields > self.max_shields:
            self.shields = self.max_shields
        
        
        self.engine_blip_time += timestep
        if self.engine_blip_time > 10:
            self.engine_blip_time = 10
        if self.engine_points and (self.accel[0] != 0 or self.accel[1] != 0) and self.engine_blip_time > 1:
            self.engine_blip_time -= 1
            for ep in self.engine_points:
                #engine_glow = Particle(load_sprite_sheet('glowengine1_10.png', 10, 10, colorkey = -1), interval = 1)
                engine_glow = GlowParticle('circle', 10, self.engine_color, 100, interval = 1)
                
                offset = Vec2(0,0)
                offset.setXY(ep[0] - 0.5 * self.original.get_rect().width, ep[1] - 0.5 * self.original.get_rect().height)
                offset.theta += self.rotation
                offset = offset.getXY()
                engine_glow.rect.center = (self.rect.center[0] + offset[0], self.rect.center[1] + offset[1])
                engine_glow.set_rotation(self.rotation)
                context.foregroundSpriteGroup.add(engine_glow)
        
        if self.removeSelf or self.health <= 0:
            explosion = Particle(Utils.get_asset('explosion1.png'), target = self)
            context.foregroundSpriteGroup.add(explosion)
            self.remove(context)
        
    def remove(self, context = None):
        #traceback.print_stack()
        self.removeSelf = True
        if context:
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.shipSpriteGroup: context.shipSpriteGroup.remove(self)
            for hp in self.hard_points:
                if hp in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(hp)
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
            if not self.parent and not self in context.destroyedSpriteGroup:
                context.destroyedSpriteGroup.add(self)
        
        if self.parent:
            if self in self.parent.hard_points: self.parent.hard_points.remove(self)
        else:
            max_damager = None
            for damager in self.stats['damaged-by'].keys():
                if not max_damager or self.stats['damaged-by'][damager] > self.stats['damaged-by'][max_damager]:
                    max_damager = damager
                    
            if max_damager:
                max_damager.stats['kills'] += 1 
            
    def collide(self, physicsEntity = None, context = None):
        pass
        if physicsEntity: # decrement shields and health here
            if isinstance(physicsEntity, Bullet): # a bullet hit the ship
                damage = self.take_damage(physicsEntity.damage)
                if physicsEntity.parent:
                    if physicsEntity.parent in self.stats['damaged-by']:
                        self.stats['damaged-by'][physicsEntity.parent] += damage
                    else:
                        self.stats['damaged-by'][physicsEntity.parent] = damage
            else: # something else hit the ship
                damage = 10
                self.take_damage(damage)
                if isinstance(physicsEntity, Ship):
                    if physicsEntity in self.stats['damaged-by']:
                        self.stats['damaged-by'][physicsEntity] += damage
                    else:
                        self.stats['damaged-by'][physicsEntity] = damage
        
        
            
                
                    
    def take_damage(self, damage = 0):
        self.shields -= damage
        if(self.shields < 0):
            hdamage = -1 * self.shields
            if self.armor >= hdamage: hdamage = 1
            else: hdamage -= self.armor
            diff = -1 * self.shields - hdamage
            damage -= diff
            self.health -= hdamage
            self.shields = 0
        
        
        
        if self.parent and self in self.parent.hard_points:
            self.parent.stats['damage-taken'] += damage
        else:
            self.stats['damage-taken'] += damage
            
        return damage
            
        #print "taking damage: " + str(damage) + ", health/shields: " + str(self.health) + "/" + str(self.shields)
        
    def apply_upgrade(self, upgrade):
        self.health += upgrade.health
        self.max_health += upgrade.health
        self.hregen += upgrade.hregen
        if self.max_shields > 0:
            self.shields += upgrade.shields
            self.max_shields += upgrade.shields
            self.sregen += upgrade.sregen
        self.armor += upgrade.armor
        if self.speed > 0:
            self.speed += upgrade.speed
        self.turn += upgrade.turn
        
        if self.weapons:
            for wp in self.weapons:
                wp.base_damage += upgrade.damage
                
        if self.hard_points:
            for hp in self.hard_points:
                hp.apply_upgrade(upgrade)

        
class ShipListXMLParser(handler.ContentHandler):
    shipList = None
    ship = None
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.shipList = []
    
    def loadShipList(self, filename = None):
        if not filename:
            filename = os.path.join("assets","shiplist.xml")
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
            self.ship.engine_color = attrs.get('engine-color', None)
            self.ship.player_flyable = attrs.get('flyable', False)
            
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
            
        elif name == "point":
            if not self.ship.hard_points:
                self.ship.hard_points = []
            self.ship.hard_points.append({'id': int(attrs.get('id')), 'x': int(attrs.get('x')), 'y': int(attrs.get('y')), 'rot': float(attrs.get('rot'))})
            
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass
    
class UpgradeListXMLParser(handler.ContentHandler):
    upgradeList = None
    ugrade = None
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.upgradeList = []
        
    def load_upgrades(self, filename = None):
        if not filename:
            filename = os.path.join('assets', 'upgrades.xml')
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
        return self.upgradeList
    
    def startElement(self, name, attrs):
        if name == "upgradelist":
            self.upgradeList = []
        elif name == "upgrade":
            self.upgrade = Upgrade(attrs)
            self.upgradeList.append(self.upgrade)
    
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass