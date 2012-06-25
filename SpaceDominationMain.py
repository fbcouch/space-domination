'''
Created on Apr 28, 2012

@author: Jami
'''

from Mission import *
from Physics import *
from Ship import Ship, Bullet, PShip, Weapon
from pygame.locals import *
from PhysicsEntity import PhysicsEntity
import Utils
import os
import pygame
import random
import sys


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
    
    playerShip = None
    
    fpstext = None
    
    lastTick = 0
    timeTotal = 0
    clock = None
    screen = None
    screen_buffer = None
    window = None
    background = None
    
    defaultfont = None
    
    rootSprite = None
    
    shipSpriteGroup = None
    backgroundSpriteGroup = None
    triggerList = []
    foregroundSpriteGroup = None

    
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
        
        self.rootSprite = pygame.sprite.OrderedUpdates()
        self.shipSpriteGroup = pygame.sprite.RenderClear()
        self.backgroundSpriteGroup = pygame.sprite.RenderClear()
        self.foregroundSpriteGroup = pygame.sprite.RenderClear()
        
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
        
        
        
        
        '''# TODO: temporarily just spawn a background and a "player ship" and have the player ship start forward
        
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
        '''
        
        self.gameState = SpaceDominationMain.GAMESTATE_NONE
        # TODO: show the menu
        # eventually the menu will lead to...
        self.gameState = SpaceDominationMain.GAMESTATE_RUNNING
        self.currentMission = self.loadMission("assets/mission01.xml")
        self.buildMission(self.currentMission)
        
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
                    elif event.key == K_SPACE:
                        self.setKey("fire", 1)
                        
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        self.setKey("accel", 0)
                    elif event.key == K_DOWN:
                        self.setKey("brake", 0)
                    elif event.key == K_LEFT:
                        self.setKey("turnLeft", 0)
                    elif event.key == K_RIGHT:
                        self.setKey("turnRight", 0)
                    elif event.key == K_SPACE:
                        self.setKey("fire",0)
                        
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
    
    def buildMission(self, mission):
        #convert spawns to player or enemy
        for spawn in mission.spawnList:
            
            if spawn.ID == -1: # this is the player ship
                tp = PShip()
                tp.file = "redfighter0jv.png" # todo - obviously we should load this in a player-specific manner
                tempShip = Ship(proto = tp)
                self.playerShip = tempShip
            else:
                tempShip = Ship()
            self.shipSpriteGroup.add(tempShip)
            self.physics.addChild(tempShip)
            tempShip.set_position(spawn.x, spawn.y)
            tempShip.set_rotation(spawn.r)
            
        #convert bglist to backgrounds
        for bg in mission.backgroundList:
            tempBg = pygame.sprite.Sprite()
            tempBg.image, tempBg.rect = Utils.load_image(bg.filename)
            tempBg.rect.topleft = (bg.x, bg.y)
            self.backgroundSpriteGroup.add(tempBg)
        
        #add the trigger list
        self.triggerList = mission.triggerList
        
        return
    
    def gameLoop(self):
        dt = self.clock.tick(30)
        self.timeTotal += dt
        
        # display the FPS
        if dt > 0: 
            self.fpstext = self.defaultfont.render("FPS: " + str(float(int(10000.0 / dt)) / 10), 1, (0, 250, 0))
            
        if not self.GAMESTATE_RUNNING:
            return True
        
        
        # TODO: implement an actual game loop
        
        
        
        # Process inputs
        if(self.playerShip):
            if(self.keys["accel"]): self.playerShip.accelerate(self.playerShip.speed * 0.25) 
                
            if(self.keys["brake"]): self.playerShip.brake(self.playerShip.speed * 0.25)
            
            if not (self.keys["accel"] or self.keys["brake"]): self.playerShip.accel = (0,0)
            
            if(self.keys["turnLeft"]): self.playerShip.set_rotation(self.playerShip.get_rotation() + 5)
            if(self.keys["turnRight"]): self.playerShip.set_rotation(self.playerShip.get_rotation() - 5)
            
            if(self.keys["fire"]): 
                bullet = self.playerShip.fire_weapon(self.timeTotal)
                if not (bullet is None):
                    self.physics.addChild(bullet)
                    self.foregroundSpriteGroup.add(bullet)
            
            
        # do physics
        
        if pygame.time.get_ticks() - self.lastTick > 33:
            self.physics.updatePhysics()
            self.lastTick = pygame.time.get_ticks()
        
            
        # decrement bullet lifetimes'
        for bullet in self.foregroundSpriteGroup:
                        
            if isinstance(bullet,Bullet):
                #bullet = (Bullet)sprite
                bullet.ticks_remaining -= 1
                if bullet.ticks_remaining <= 0:
                    self.physics.physicsChildren.remove(bullet)           
                    self.foregroundSpriteGroup.remove(bullet)     
                    
            # remove any colliders
            if isinstance(bullet,PhysicsEntity):
                if bullet.removeSelf:
                    if bullet in self.physics.physicsChildren: self.physics.physicsChildren.remove(bullet)
                    if bullet in self.foregroundSpriteGroup: self.foregroundSpriteGroup.remove(bullet)
        
        for sprite in self.shipSpriteGroup:
            if isinstance(sprite,PhysicsEntity):
                if sprite.removeSelf:
                    if sprite in self.physics.physicsChildren: self.physics.physicsChildren.remove(sprite)
                    if sprite in self.shipSpriteGroup: self.shipSpriteGroup.remove(sprite)
                    
        maxrect = Rect(0,0,0,0)
        for sprite in self.backgroundSpriteGroup: # backgrounds will define the boundaries
            if sprite.rect.left + sprite.rect.width > maxrect.width:
                maxrect.width = sprite.rect.left + sprite.rect.width
            if sprite.rect.top + sprite.rect.height > maxrect.height:
                maxrect.height = sprite.rect.top + sprite.rect.height
            
        self.screen_buffer = pygame.Surface((maxrect.width, maxrect.height))
        
        
        # clear the background (blit a blank screen) then draw everything in the background then the sprite groups then the foreground group
        self.screen.blit(self.background, (0,0))
        #self.rootSprite.clear(self.screen, self.background)
        #self.rootSprite.draw(self.screen)
        #self.backgroundSpriteGroup.clear(self.screen, self.background)
        self.backgroundSpriteGroup.draw(self.screen_buffer)
        #self.shipSpriteGroup.clear(self.screen, self.background)
        self.shipSpriteGroup.draw(self.screen_buffer)
        self.foregroundSpriteGroup.draw(self.screen_buffer)
        
        
        # now render to the screen using the playerShip to decide on coords
        render = (-1 * self.playerShip.rect.center[0] + (self.screen.get_width() * 0.5), -1 * self.playerShip.rect.center[1] + (self.screen.get_height() * 0.5))
        if render[0] > 0: render = (0, render[1])
        if render[1] > 0: render = (render[0], 0)
        if render[0] < -1 * maxrect.width + self.screen.get_width(): render = (-1 * maxrect.width + self.screen.get_width(), render[1])
        if render[1] < -1 * maxrect.height + self.screen.get_height(): render = (render[0], -1 * maxrect.height + self.screen.get_height())
        self.screen.blit(self.screen_buffer, render)
        
        
        self.screen.blit(self.fpstext, (10,10))
        pygame.display.flip()
        
        return True
    
#the main entry point for the program
app = SpaceDominationMain()
app.run()