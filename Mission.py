'''
Created on May 5, 2012

@author: Jami
'''

from Ship import PShip, Ship
from Trigger import CreateTrigger, Trigger
from Utils import load_image
from xml.sax import saxutils, handler, make_parser
import os

class Mission(object):
    # this will be the main class that the missions will be loaded into and will contain info on spawning backgrounds, ships, triggers, etc
    missionName = ""
    missionDesc = ""
    backgroundList = None
    spawnList = None
    triggerList = None
    
    icon = None
    
    initialized = False
    
    width = 0
    height = 0
    background_style = None #'tiled' or ??
    background_file = None
    
    isCampaignMission = False
    
    def __init__(self):
        self.backgroundList = []
        self.spawnList = []
        self.triggerList = []
    
    def update(self, context = None, timestep = 1):
        pass
    
    def build(self):
        pass
    
    def toXML(self):
        returnVal = "<mission name=\"" + self.missionName + "\" desc=\"" + self.missionDesc + "\">\n"
        for bg in self.backgroundList:
            returnVal += bg.toXML() + "\n"
        for sp in self.spawnList:
            returnVal += sp.toXML() + "\n"
        for tg in self.triggerList:
            returnVal += tg.toXML() + "\n"
        returnVal += "</mission>"
        return returnVal
    
class Background(object):
    filename = ""
    x = 0
    y = 0
    scale = 0

    def toXML(self):
        return "<background file=\"" + self.filename + "\" x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" scale=\"" + str(self.scale) + "\" />"
        
class Spawn(object):
    id = 0
    x = 0
    y = 0
    r = 0
    tag = ""
    
    type = 'enemy'
    
    proto = None
    hard_points = None
    
    squad = None
    
    def __init__(self):
        self.hard_points = []
    
    def toXML(self):
        returnString = "<"
        if self.id == -1: returnString += "playerspawn"
        else: returnString += "enemy id=\"" + str(self.id) + "\""
        returnString += " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" rot=\"" + str(self.r) + " tag=\"" + self.tag + "\" />"
        return returnString
    


class MissionXMLParser(handler.ContentHandler):
    
    loadedMission = None
    inPlayerSpawn = False
    inEnemy = False
    inBackground = False
    inTrigger = False
    inPoint = False
    inAlly = False
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.loadedMission = Mission()
        
    def loadMission(self, filename = "mission01.xml"):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(os.path.join("assets", filename))
        return self.loadedMission
          
    def startElement(self, name, attrs):
        # beginning of an element that encloses others & may have attributes (process here)
        if name == "mission":
            self.loadedMission = Mission()
            if 'width' in attrs: self.loadedMission.width = int(attrs.get('width'))
            if 'height' in attrs: self.loadedMission.height = int(attrs.get('height'))
            if 'background-style' in attrs: self.loadedMission.background_style = attrs.get('background-style')
            if 'background-file' in attrs: self.loadedMission.background_file = attrs.get('background-file')
            
            
        elif name == "background":
            newBackground = Background()
            
            newBackground.filename = attrs.get('file','')
            newBackground.x = float(attrs.get('x',''))
            newBackground.y = float(attrs.get('y',''))
            newBackground.scale = float(attrs.get('scale',''))
            self.loadedMission.backgroundList.append(newBackground)
            
            self.inBackground = True
        elif name == "playerspawn":
            newSpawn = self.spawn_from_attrs(attrs)
            
            newSpawn.type = 'player'
            newSpawn.team = Ship.TEAM_DEFAULT_FRIENDLY
            newSpawn.id = -1
            self.loadedMission.spawnList.append(newSpawn)
            
            self.inPlayerSpawn = True
        elif name == "enemy":
            newSpawn = self.spawn_from_attrs(attrs)
            newSpawn.type = 'enemy'
            newSpawn.team = Ship.TEAM_DEFAULT_ENEMY
            
            self.loadedMission.spawnList.append(newSpawn)
            
            self.inEnemy = True
        elif name == "ally":
            newSpawn = self.spawn_from_attrs(attrs)
            newSpawn.type = 'friendly'
            newSpawn.team = Ship.TEAM_DEFAULT_FRIENDLY
            
            self.loadedMission.spawnList.append(newSpawn)
            
            self.inAlly = True
        elif name == "trigger":
            tg = CreateTrigger(int(attrs.get('id')), 
                               attrs.get('type',''),
                               attrs.get('condition',''), 
                               attrs.get('attrs',''), attrs.get('tag',''), 
                               attrs.get('display-text',''), 
                               attrs.get('message-icon',''),
                               attrs.get('message-title',''),
                               attrs.get('message-body',''))
            
            # TODO allow a trigger to link to a hard point
            #if self.inPoint:
            #    cspawn = self.loadedMission.spawnList[len(self.loadedMission.spawnList) - 1]
            #    tg.parent = cspawn.hard_points[len(cspawn.hard_points) - 1]
            if self.inPlayerSpawn or self.inEnemy or self.inAlly:
                tg.parent = self.loadedMission.spawnList[len(self.loadedMission.spawnList) - 1]
            
            
            self.loadedMission.triggerList.append(tg)
                        
            self.inTrigger = True
        elif name == "point":
            if self.inEnemy or self.inPlayerSpawn or self.inAlly:
                newSpawn = self.spawn_from_attrs(attrs)
                self.loadedMission.spawnList[len(self.loadedMission.spawnList)-1].hard_points.append(newSpawn)
                
            self.inPoint = True
                
        return
        
    def endElement(self, name):
        # end of an element
        if name == "background":
            self.inBackground = False
        elif name == "playerspawn":
            self.inPlayerSpawn = False
        elif name == "enemy":
            self.inEnemy = False
        elif name == "ally":
            self.inAlly = False
        elif name == "trigger":
            self.inTrigger = False
        elif name == "point":
            self.inPoint = False
            
        return
        
    def characters(self, content):
        # handle plain text
        return
    
    def getMission(self): return self.loadedMission
    
    def spawn_from_attrs(self, attrs):
        newSpawn = Spawn()
        newSpawn.id = int(attrs.get('id', '-1'))
        newSpawn.x = float(attrs.get('x',''))
        newSpawn.y = float(attrs.get('y',''))
        newSpawn.r = float(attrs.get('rot',''))
        newSpawn.tag = attrs.get('tag','')
        
        # proto stuff
        newProto = PShip()
        if 'name' in attrs: newProto.name = attrs.get('name')
        if 'file' in attrs: newProto.file = attrs.get('file')
        if 'health' in attrs: newProto.health = int(attrs.get('health'))
        if 'hregen' in attrs: newProto.hregen = float(attrs.get('hregen'))
        if 'shields' in attrs: newProto.shields = int(attrs.get('shields'))
        if 'sregen' in attrs: newProto.sregen = float(attrs.get('sregen'))
        if 'speed' in attrs: newProto.speed = float(attrs.get('speed'))
        if 'turn' in attrs: newProto.turn = float(attrs.get('turn'))
        if 'armor' in attrs: newProto.armor = float(attrs.get('armor'))
        newSpawn.proto = newProto
        
        return newSpawn
            
        
class MissionListXMLParser(handler.ContentHandler):
    missionList = None
    inMission = False
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.missionList = []
    
    def loadMissionList(self, filename = "assets/missions.xml"):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
        return self.missionList
    
    def startElement(self, name, attrs):
        if name == "missionlist":
            self.missionList = []
        elif name == "mission":
            mission = []
            mission.append(attrs.get('file',''))
            image_file = attrs.get('icon','')
            
            if not(image_file == None):
                try:
                    image, rect = load_image(image_file, colorkey = -1)
                except SystemExit, message:
                    image = None
                    print "Error loading file: " + image_file
                mission.append(image)
            else:
                mission.append(None)
                
            mission.append(attrs.get('name',''))
            mission.append('') # description
            self.missionList.append(mission)
            
            self.inMission = True
    
    def endElement(self, name):
        if name == "mission":
            self.inMission = False
    
    def characters(self, content):
        if self.inMission: self.missionList[len(self.missionList) - 1][3] += content
    
    