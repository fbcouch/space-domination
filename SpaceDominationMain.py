'''
Created on Apr 28, 2012

@author: Jami
'''

from Mission import *
from Ship import *
from Physics import *
import Utils
import pygame, sys, os, random
from pygame.locals import *


class SpaceDominationMain():
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
    
    lastTick = 0
    clock = None
    screen = None
    window = None
    background = None
    
    defaultfont = None
    
    rootSprite = None
    
    def __init__(self):
        '''
        Constructor
        '''
        #initialize managers
        pygame.init()
        random.seed()
        self.window = pygame.display.set_mode((1024,768))
        pygame.display.set_caption("Space Domination")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        self.rootSprite = pygame.sprite.RenderClear()
        
        if pygame.font:
            self.defaultfont = pygame.font.Font(None, 20)
        
        # TODO: implement loading splash screen
        self.showSplash()
        # TODO: implement menu manager
        self.loadMenus()
        # TODO: implement loading game assets
        self.loadMissionList()
        # TODO: implement physics manager
        self.physics = Physics()
        
        # setup keymap
        self.keys = {"turnLeft" : 0, "turnRight" : 0, "accel" : 0, "brake" : 0, "fire" : 0, "alt-fire" : 0}
        
        
        
        self.removeSplash()
        
        
        
        
        # TODO: temporarily just spawn a background and a "player ship" and have the player ship start forward
        self.tempPlayerShip = Ship(parent = self.rootSprite)
        self.tempPlayerShip.set_position(100, 100)
        self.physics.addChild(self.tempPlayerShip)
        
        #self.tempPlayerShip.set_rotation(180)
        self.rootSprite.add(self.tempPlayerShip)
        tempimg, temprect = Utils.load_image("cube_2.jpg")
        tmpSprite = pygame.sprite.Sprite()
        tmpSprite.image = tempimg
        tmpSprite.rect = temprect
        #self.rootSprite.add(tmpSprite)
        
        #self.tempPlayerShip.setVel(Vec3(1,0,0))
        self.tempPlayerShip.set_rotation(90)
        
        self.gameState = SpaceDominationMain.GAMESTATE_RUNNING
        
        
    def run(self):
        while True:
            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    elif event.key == K_UP:
                        self.setKey("accel", 1)
                    elif event.key == K_DOWN:
                        self.setKey("brake", 1)
                    elif event.key == K_LEFT:
                        self.setKey("turnLeft", 1)
                    elif event.key == K_RIGHT:
                        self.setKey("turnRight", 1)
                        
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        self.setKey("accel", 0)
                    elif event.key == K_DOWN:
                        self.setKey("brake", 0)
                    elif event.key == K_LEFT:
                        self.setKey("turnLeft", 0)
                    elif event.key == K_RIGHT:
                        self.setKey("turnRight", 0)
                        
            # game loop
            self.gameLoop()
        
        return
    
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
    
    def gameLoop(self):
        dt = self.clock.tick(30)
        
        
        # display the FPS
        if dt > 0: 
            self.fpstext = self.defaultfont.render("FPS: " + str(float(int(10000.0 / dt)) / 10), 1, (0, 250, 0))
            
        if not self.GAMESTATE_RUNNING:
            return True
        
        
        # TODO: implement an actual game loop
        
        
        
        # Process inputs
        if(self.tempPlayerShip):
            if(self.keys["accel"]): self.tempPlayerShip.accelerate(self.tempPlayerShip.speed * 0.25) 
                
            if(self.keys["brake"]): self.tempPlayerShip.brake(self.tempPlayerShip.speed * 0.25)
            
            if not (self.keys["accel"] or self.keys["brake"]): self.tempPlayerShip.accel = (0,0)
            
            if(self.keys["turnLeft"]): self.tempPlayerShip.set_rotation(self.tempPlayerShip.get_rotation() + 5)
            if(self.keys["turnRight"]): self.tempPlayerShip.set_rotation(self.tempPlayerShip.get_rotation() - 5)
            
            
        # do physics
        
        if pygame.time.get_ticks() - self.lastTick > 33:
            self.physics.updatePhysics()
            self.lastTick = pygame.time.get_ticks()
        
            
        
        self.screen.blit(self.background, (0,0))
        self.rootSprite.clear(self.screen, self.background)
        self.rootSprite.draw(self.screen)
        self.screen.blit(self.fpstext, (10,10))
        pygame.display.flip()
        
        return True
    
#the main entry point for the program
app = SpaceDominationMain()
app.run()
