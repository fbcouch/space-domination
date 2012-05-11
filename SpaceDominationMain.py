'''
Created on Apr 28, 2012

@author: Jami
'''

from Mission import *
from Ship import *
from Sprite import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import TextNode, NodePath, Point2, Point3
from task.TaskManagerGlobal import taskMgr
import Utils
import sys


class SpaceDominationMain(ShowBase):
    '''
    classdocs
    '''
    # game state constants
    GAMESTATE_NONE = 0
    GAMESTATE_RUNNING = 1
    GAMESTATE_PAUSED = 2
    GAMESTATE_GAMEOVER = 3
    
    gameState = GAMESTATE_NONE
    
    physics = None
    menuManager = None
    missionList = None
    currentMission = None
    
    tempPlayerShip = None
    
    fpstext = None
    
    def __init__(self):
        '''
        Constructor
        '''
        ShowBase.__init__(self)
        
        
        #initialize managers
        
        # TODO: implement loading splash screen
        self.showSplash()
        # TODO: implement menu manager
        self.loadMenus()
        # TODO: implement loading game assets
        self.loadMissionList()
        # TODO: implement physics manager
        
        # setup keymap
        self.keys = {"turnLeft" : 0, "turnRight" : 0, "accel" : 0, "brake" : 0, "fire" : 0, "alt-fire" : 0}
        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["turnLeft", 1])
        self.accept("arrow_left-up", self.setKey, ["turnLeft", 0])
        self.accept("arrow_right", self.setKey, ["turnRight", 1])
        self.accept("arrow_right-up", self.setKey, ["turnRight", 0])
        self.accept("arrow_up", self.setKey, ["accel", 1])
        self.accept("arrow_up-up", self.setKey, ["accel", 0])
        self.accept("arrow_down", self.setKey, ["brake", 1])
        self.accept("arrow_down-up", self.setKey, ["brake", 0])
        self.accept("space", self.setKey, ["fire", 1])
        self.accept("space-up", self.setKey, ["fire", 0])
        self.accept("shift", self.setKey, ["shift", 1])
        self.accept("shift-up", self.setKey, ["shift", 0])
        
        
        self.removeSplash()
        
        
        # TODO: temporarily just spawn a background and a "player ship" and have the player ship start forward
        Sprite(Utils.loadObject(tex = "gfx/default_background.png", parent = camera, pos = Point2(0,0), scale = 10), rotation = 0)
        self.tempPlayerShip = Ship(parent = camera)
        self.tempPlayerShip.setVel(Vec3(1,0,0))
        
        self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")
        self.gameTask.last = 0
        
        self.gameState = SpaceDominationMain.GAMESTATE_RUNNING
        
        
    def setKey(self, key, val): self.keys[key] = val
        
        
    def showSplash(self):
        # TODO: show splash screen
        
        
        return
        
    def removeSplash(self):
        # TODO: remove splash screen
        
        return
    
    def loadMenus(self):
        
        return
    
    def loadMissionList(self):
        
        return
    
    def loadMission(self, filename):
    
        return MissionXMLParser().loadMission(filename)
    
    def gameLoop(self, task):
        
        #get the amount of time changed
        dt = task.time - task.last
        task.last = task.time
        
        #test cap FPS at 30
        if dt < 0.0333: 
            task.last -= dt
            return Task.cont
        
        
        # display the FPS
        if dt > 0: 
            if not self.fpstext is None: self.fpstext.remove()
            self.fpstext = Utils.genLabelText("FPS: " + str(float(int(10 / dt)) / 10), 0)
        
        if not self.GAMESTATE_RUNNING:
            return Task.cont
        
        
        # TODO: implement an actual game loop
        
        
        
        # for now, just move the test sprite around
        if(self.tempPlayerShip):
            if(self.keys["accel"]): self.tempPlayerShip.setPos(Point2(self.tempPlayerShip.getPos().getX(), self.tempPlayerShip.getPos().getY() + 1))
            if(self.keys["brake"]): self.tempPlayerShip.setPos(Point2(self.tempPlayerShip.getPos().getX(), self.tempPlayerShip.getPos().getY() - 1))
            if(self.keys["turnLeft"]): self.tempPlayerShip.setR(self.tempPlayerShip.getR() - 5)
            if(self.keys["turnRight"]): self.tempPlayerShip.setR(self.tempPlayerShip.getR() + 5)
            
            
        return Task.cont
    
#the main entry point for the program
app = SpaceDominationMain()
app.run()
