'''
Created on Jul 4, 2012

@author: Jami
'''
from xml.sax import handler, make_parser
from Utils import *

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
    
    image_file = None
    image = None
    
    def __init__(self):
        pass
    
    def can_fire(self, time):
        if (self.cur_ammo > 0 and time > self.last_fire + self.fire_rate):
            return True
        return False
    
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
    