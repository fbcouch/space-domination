'''
Created on May 5, 2012

@author: Jami
'''

from Trigger import CreateTrigger, Trigger
from Utils import load_image
from xml.sax import saxutils, handler, make_parser
import os

class Mission(object):
    # this will be the main class that the missions will be loaded into and will contain info on spawning backgrounds, ships, triggers, etc
    missionName = ""
    missionDesc = ""
    backgroundList = []
    spawnList = []
    triggerList = []
    
    def __init__(self):
        # TODO something?
        return
    
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
    
    def toXML(self):
        returnString = "<"
        if self.id == -1: returnString += "playerspawn"
        else: returnString += "enemy id=\"" + str(self.id) + "\""
        returnString += " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" rot=\"" + str(self.r) + "\" />"
        return returnString
    


class MissionXMLParser(handler.ContentHandler):
    
    loadedMission = None
    inPlayerSpawn = False
    inEnemy = False
    inBackground = False
    inTrigger = False
    
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
            
        elif name == "background":
            newBackground = Background()
            
            newBackground.filename = attrs.get('file','')
            newBackground.x = float(attrs.get('x',''))
            newBackground.y = float(attrs.get('y',''))
            newBackground.scale = float(attrs.get('scale',''))
            self.loadedMission.backgroundList.append(newBackground)
            
            self.inBackground = True
        elif name == "playerspawn":
            newSpawn = Spawn()

            newSpawn.x = float(attrs.get('x',''))
            newSpawn.y = float(attrs.get('y',''))
            newSpawn.r = float(attrs.get('rot',''))
            newSpawn.id = -1
            self.loadedMission.spawnList.append(newSpawn)
            
            self.inPlayerSpawn = True
        elif name == "enemy":
            newSpawn = Spawn()
            
            newSpawn.id = int(attrs.get('id',''))
            newSpawn.x = float(attrs.get('x',''))
            newSpawn.y = float(attrs.get('y',''))
            newSpawn.r = float(attrs.get('rot',''))
            
            self.loadedMission.spawnList.append(newSpawn)
            
            self.inEnemy = True
        elif name == "trigger":
            tg = CreateTrigger(int(attrs.get('id')), 
                               attrs.get('type',''),
                               attrs.get('condition',''), 
                               attrs.get('attrs',''), attrs.get('tag',''), 
                               attrs.get('display-text',''), 
                               attrs.get('message-icon',''),
                               attrs.get('message-title',''),
                               attrs.get('message-body',''))
            if self.inPlayerSpawn or self.inEnemy:
                tg.parent = self.loadedMission.spawnList[len(self.loadedMission.spawnList) - 1]               
            
            self.loadedMission.triggerList.append(tg)
            
            # TODO remove this
            print "Trigger:"
            print "\tid=" + str(tg.id)
            print "\tcondition=" + tg.condition
            if tg.parent:
                print "\tparent=" + str(tg.parent.id)
            else:
                print "\tparent=None"
            
            self.inTrigger = True
        return
        
    def endElement(self, name):
        # end of an element
        if name == "background":
            self.inBackground = False
        elif name == "playerspawn":
            self.inPlayerSpawn = False
        elif name == "enemy":
            self.inEnemy = False
        elif name == "trigger":
            self.inTrigger = False
            
        return
        
    def characters(self, content):
        # handle plain text
        return
    
    def getMission(self): return self.loadedMission
        
        
class MissionListXMLParser(handler.ContentHandler):
    missionList = None
    
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
            self.missionList.append(mission)
    
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass
    
    