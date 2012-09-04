'''
Created on Jul 4, 2012

@author: Jami
'''
from Bullet import Bullet
from Utils import *
from Vec2 import Vec2
from xml.sax import handler, make_parser
import Utils
import consts

class Weapon(object):
    id = 0
    name = ""
    
    max_ammo = 0
    cur_ammo = 0
    ammo_regen = 0
    fire_rate = 0
    last_fire = 0
    base_damage = 0
    bullet_ticks = 100
    bullet_speed = 20
    type = "laser" # laser or missile
    
    fire_points = None
    
    image_file = None
    image = None
    
    engines = None
    engine_color = None
    
    def __init__(self):
        pass
    
    def can_fire(self):
        
        if not self.fire_points or len(self.fire_points) == 0: 
            points = 1
        else:
            points = len(self.fire_points)
        if (self.cur_ammo >= points and self.last_fire > self.fire_rate):
            return True
        return False
    
    def update(self, context, timestep = 1):
        self.last_fire += timestep
    
    def fire(self, time, parent, sprite, rotation, velocity):
        '''fire the weapon if possible given (time)'''
        weapon = self
        bullets = []
        if self.can_fire():
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
                    
                bullet.parent = parent
                
                if weapon.fire_points and len(weapon.fire_points) > n:
                    # move the bullet to the specified point
                    offset = Vec2(0,0)
                    offset.setXY(weapon.fire_points[n][0] - sprite.original.get_rect().width * 0.5 + bullet.rect.width, weapon.fire_points[n][1] - sprite.original.get_rect().height * 0.5)
                    offset.theta += rotation
                    offset = offset.getXY()
                    bullet.rect.center = sprite.rect.center
                    bullet.rect.topleft = bullet.rect.left + offset[0], bullet.rect.top + offset[1]
                    bullet.position = bullet.rect.topleft
                    
                else:
                    # move the bullet to the center-front of the ship
                    bullet.rect.center = sprite.rect.left + sprite.rect.width * 0.5, sprite.rect.top + sprite.rect.height * 0.5
                    offset = Vec2(sprite.rect.height * 0.5 + bullet.rect.width, rotation)
                    offset = offset.getXY()
                    bullet.rect.topleft = bullet.rect.left + offset[0], bullet.rect.top + offset[1]
                    bullet.position = bullet.rect.topleft
                
                if self.engines:
                    bullet.engine_points = self.engines
                    bullet.engine_color = self.engine_color
                
                bullet.original = bullet.image
                bullet.set_rotation(rotation)
                    
                # match the bullet and ship velocities
                if not self.type or self.type == 'laser':
                    vel1 = Vec2(weapon.bullet_speed, rotation)
                elif self.type == 'missile':
                    # missiles start with just the ship velocity
                    vel1 = Vec2(0,0)
                    bullet.max_vel_sq = (weapon.bullet_speed) **2
                    # also add some accel to the missile
                    acc = Vec2(weapon.bullet_speed * 0.1, rotation)
                    bullet.accel = acc.getXY()
                    vel2 = Vec2(0,0)
                    vel2.setXY(velocity[0], velocity[1])
                    vel1 = vel1.add(vel2)
                else:
                    vel1 = Vec2(weapon.bullet_speed, rotation)
                
                bullet.velocity = vel1.getXY()#vel1.getXY()
                
                
                
            
                # increment weapon stuff
                weapon.cur_ammo -= 1
                weapon.last_fire = 0
            
                # set up the bullet lifetime info
                bullet.ticks_remaining = weapon.bullet_ticks
                bullet.damage = weapon.base_damage
                bullet.type = weapon.type
                
                n += 1
        return bullets
    
    def set_points(self, pointlist):
        self.fire_points = Utils.parse_pointlist(pointlist)
        
        
    def toXML(self):
        return ("<weapon id='" + str(self.id) + "' name='" + self.name + 
                "' ammo='" + str(self.max_ammo) + "' regen='" + 
                str(self.ammo_regen) + "' rate='" + str(self.fire_rate) + 
                "' damage='" + str(self.base_damage) + "' life='" + 
                str(self.bullet_ticks) + "' speed='" + str(self.bullet_speed) +
                "' />")
    
    def clone(self):
        returnVal = Weapon()
        returnVal.id = self.id
        returnVal.name = self.name
        returnVal.max_ammo = self.max_ammo
        returnVal.cur_ammo = self.cur_ammo
        returnVal.ammo_regen = self.ammo_regen
        returnVal.fire_rate = self.fire_rate
        returnVal.last_fire = self.last_fire
        returnVal.base_damage = self.base_damage
        returnVal.bullet_ticks = self.bullet_ticks
        returnVal.bullet_speed = self.bullet_speed
        returnVal.image_file = self.image_file
        returnVal.image = self.image
        returnVal.type = self.type
        returnVal.engines = self.engines
        returnVal.engine_color = self.engine_color
        return returnVal
    
class WeaponListXMLParser(handler.ContentHandler):
    weaponList = None
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.missionList = []
    
    def loadWeaponList(self, filename = "assets/weaponlist.xml"):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
        return self.weaponList
    
    def startElement(self, name, attrs):
        if name == "weaponlist":
            self.weaponList = []
        elif name == "weapon":
            weapon = Weapon()
            
            weapon.id = int(attrs.get('id'))
            weapon.max_ammo = int(attrs.get('ammo', '100'))
            weapon.cur_ammo = weapon.max_ammo
            weapon.ammo_regen = float(attrs.get('regen', '2'))
            weapon.base_damage = int(attrs.get('damage', '10'))
            weapon.fire_rate = int(attrs.get('rate', '2'))
            weapon.bullet_speed = float(attrs.get('speed', '6'))
            weapon.bullet_ticks = int(attrs.get('life', '10'))
            weapon.name = attrs.get('name', 'Unnamed Weapon')   
            weapon.type = attrs.get('type', 'laser')    
            engines = attrs.get('engines', None)
            
            if engines:
                weapon.engines = Utils.parse_pointlist(engines)
            color = attrs.get('engine-color', 'orange')
            if color in consts.colors:
                weapon.engine_color = consts.colors[color]
            else:
                weapon.engine_color = consts.COLOR_ORANGE
            
            weapon.image_file = attrs.get('file','')
            
            
            if not(weapon.image_file == None):
                try:
                    image, rect = load_image(weapon.image_file, colorkey = -1)
                except SystemExit, message:
                    image = None
                    print "Error loading file: " + weapon.image_file
                weapon.image = image
            else:
                weapon.image = None
            self.weaponList.append(weapon)
            
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass
    