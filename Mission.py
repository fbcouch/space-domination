'''
Created on May 5, 2012

@author: Jami
'''

from xml.sax import saxutils, handler, make_parser

class Mission:
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
    
class Background:
    filename = ""
    x = 0
    y = 0
    scale = 0

    def toXML(self):
        return "<background file=\"" + self.filename + "\" x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" scale=\"" + str(self.scale) + "\" />"
        
class Spawn:
    ID = 0
    x = 0
    y = 0
    r = 0
    
    def toXML(self):
        returnString = "<"
        if self.ID == -1: returnString += "playerspawn"
        else: returnString += "enemy id=\"" + str(self.ID) + "\""
        returnString += " x=\"" + str(self.x) + "\" y=\"" + str(self.y) + "\" rot=\"" + str(self.r) + "\" />"
        return returnString
    
class Trigger:
    # TODO implement triggers
    def toXML(self):
        return "<trigger />"

class MissionXMLParser(handler.ContentHandler):
    
    loadedMission = None
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.loadedMission = Mission()
        
    def loadMission(self, filename = "assets/mission01.xml"):
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
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
                
        elif name == "playerspawn":
            newSpawn = Spawn()

            newSpawn.x = float(attrs.get('x',''))
            newSpawn.y = float(attrs.get('y',''))
            newSpawn.r = float(attrs.get('rot',''))
            newSpawn.ID = -1
            self.loadedMission.spawnList.append(newSpawn)
            
        elif name == "enemy":
            newSpawn = Spawn()
            
            newSpawn.ID = int(attrs.get('id',''))
            newSpawn.x = float(attrs.get('x',''))
            newSpawn.y = float(attrs.get('y',''))
            newSpawn.r = float(attrs.get('rot',''))
            
            self.loadedMission.spawnList.append(newSpawn)
        elif name == "trigger":
            self.loadedMission.triggerList.append(Trigger())
        
        return
        
    def endElement(self, name):
        # end of an element
        return
        
    def characters(self, content):
        # handle plain text
        return
    
    def getMission(self): return self.loadedMission
        