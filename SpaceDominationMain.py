'''
Created on Apr 28, 2012

@author: Jami
'''

from AIShip import AIShip
from Menu import MenuManager
from Mission import *
from Particle import Particle
from Physics import *
from PhysicsEntity import PhysicsEntity
from PlayerShip import PlayerShip
from Ship import Ship, PShip, Weapon, ShipListXMLParser
from Utils import load_sprite_sheet
from Weapon import WeaponListXMLParser
from hud import HUD
from pygame.locals import *
import Menu
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
    weaponList = None
    shipList = None
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
    menuBackground = None
    
    defaultfont = None
    largefont = None
    
    rootSprite = None
    
    shipSpriteGroup = None
    backgroundSpriteGroup = None
    triggerList = None
    foregroundSpriteGroup = None
    
    messageList = None
    
    HUD = None
    
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
        self.triggerList = []
        self.messageList = []
        
        if pygame.font:
            self.defaultfont = pygame.font.Font(None, 20)
            self.largefont = pygame.font.Font(os.path.join("assets", "PLANM___.TTF"), 40)
        
        # load the mission list
        self.missionList = self.loadMissionList()
        
        # load the menus
        self.menuManager = MenuManager(self.screen, self)
        
        # load & display splash screen
        self.showSplash()
        splashTime = pygame.time.get_ticks()
        
        # load weapons
        self.weaponList = WeaponListXMLParser().loadWeaponList()
        
        
        # load ships
        self.shipList = ShipListXMLParser().loadShipList()
        
        
        # initialize physics manager
        self.physics = Physics()
        
        # setup keymap
        self.keys = {"turnLeft" : 0, "turnRight" : 0, "accel" : 0, "brake" : 0, "fire" : 0, "alt-fire" : 0}
        
        
        # load the HUD
        self.HUD = HUD()
        
        # allow the splash to show for no less than 5 seconds, but any time between here and there counts
        pygame.time.wait(5000 - pygame.time.get_ticks() - splashTime)
        self.removeSplash()
        
        
        
        
        
        
        self.gameState = SpaceDominationMain.GAMESTATE_NONE
        self.menuBackground = load_image("background.PNG")[0]
        self.menuManager.menu_state_parse(Menu.MENU_MAIN)
        # TODO: show the menu
        # eventually the menu will lead to...
        #self.gameState = SpaceDominationMain.GAMESTATE_RUNNING
        #self.currentMission = self.loadMission("mission01.xml")
        #self.buildMission(self.currentMission)
        
    def run(self):
        rect_list = []
        while True:
            # handle input
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if self.menuManager.is_active():
                        self.menuManager.update(event)
                        if self.menuManager.selectedMenu == -1 and self.gameState == self.GAMESTATE_PAUSED: self.gameState = self.GAMESTATE_RUNNING
                    elif event.key == K_ESCAPE:
                        if self.gameState == self.GAMESTATE_RUNNING:
                            self.gameState = self.GAMESTATE_PAUSED
                            self.menuManager.menu_state_parse(Menu.MENU_PAUSE)
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

            
            # clear the background (blit a blank screen) then draw everything in the background then the sprite groups then the foreground group
            self.screen.blit(self.background, (0,0))
            
            # game loop
            self.gameLoop()
            if self.gameState == self.GAMESTATE_NONE:
                self.screen.blit(self.menuBackground, (0,0))
            if self.menuManager.is_active(): self.menuManager.draw()
            pygame.display.flip()
        
        return
    
    def setKey(self, key, val): self.keys[key] = val
        
        
    def showSplash(self):
        self.screen.blit(self.background,  (0, 0))
        splashImage,  splashRect = Utils.load_image("splash.png")
        centerScreen = (self.screen.get_size()[0] * 0.5,  self.screen.get_size()[1] * 0.5)
        self.screen.blit(splashImage,  (centerScreen[0] - splashRect.width * 0.5, centerScreen[1] - splashRect.height * 0.5))
        pygame.display.flip()
        
        
        return
        
    def removeSplash(self):
        self.screen.blit(self.background,  (0, 0))
        pygame.display.flip()
        
        return
    
    def loadMissionList(self):
        return MissionListXMLParser().loadMissionList()
    
    def loadMission(self, filename):
    
        return MissionXMLParser().loadMission(filename)
    
    
        
    
    def buildMission(self, mission):
        #add the trigger list
        self.triggerList = mission.triggerList
        self.rootSprite = pygame.sprite.OrderedUpdates()
        self.shipSpriteGroup = pygame.sprite.RenderClear()
        self.backgroundSpriteGroup = pygame.sprite.RenderClear()
        self.foregroundSpriteGroup = pygame.sprite.RenderClear()
        self.physics = Physics()
        self.messageList = []
        
        #convert spawns to player or enemy
        for spawn in mission.spawnList:
            
            if spawn.id == -1: # this is the player ship
                tp = PShip()
                tp.file = "redfighter0jv.png" # todo - obviously we should load this in a player-specific manner
                tp.weapons.append(0)
                tempShip = PlayerShip(proto = tp, context = self )
                self.playerShip = tempShip
                self.linkTriggers(spawn, tempShip)
            else:
                if spawn.id >= 0 and spawn.id < len(self.shipList):
                    tempShip = AIShip(proto = self.shipList[spawn.id], context = self)
                    
                    self.linkTriggers(spawn, tempShip)
            self.shipSpriteGroup.add(tempShip)
            self.physics.addChild(tempShip)
            tempShip.set_position(spawn.x, spawn.y)
            tempShip.set_rotation(spawn.r)
            tempShip.tag = spawn.tag
            
        #convert bglist to backgrounds
        for bg in mission.backgroundList:
            tempBg = pygame.sprite.Sprite()
            tempBg.image, tempBg.rect = Utils.load_image(bg.filename)
            tempBg.rect.topleft = (bg.x, bg.y)
            self.backgroundSpriteGroup.add(tempBg)
        
        
        
        return
    
    def linkTriggers(self, spawn, ship):
        for tg in self.triggerList:
            if tg.parent == spawn:
                tg.parent = ship
    
    def displayObjectives(self, screen):
        
        primary = []
        secondary = []
        maxwidth = self.defaultfont.size("Secondary Objectives")[0]
        for tg in self.triggerList:
            if tg.type.count("objective-primary") > 0:
                primary.append(tg)
            elif tg.type.count("objective-secondary") > 0:
                secondary.append(tg)
            
            w = self.defaultfont.size(tg.display_text)[0]
            if w > maxwidth: maxwidth = w
        
        
        
        y = 0
        if len(primary) > 0:
            screen.blit(self.defaultfont.render("Primary Objectives:",1,(255,255,0)), (self.screen.get_width() - maxwidth - 24, y))
            y += 20
            
        for tg in primary:
            tgstr = tg.display_text
            if tg.completed:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            screen.blit(self.defaultfont.render(tgstr,1,color), (self.screen.get_width() - maxwidth, y))
            y += 20
            
        if (len(secondary) > 0):
            screen.blit(self.defaultfont.render("Secondary Objectives:",1,(255,255,0)), (self.screen.get_width() - maxwidth - 24, y))
            y += 20
            
        for tg in secondary:
            tgstr = tg.display_text
            screen.blit(self.defaultfont.render(tgstr,1,(255,0,0)), (self.screen.get_width() - maxwidth, y))
            y += 20
            
        return
    
    def displayMessages(self, screen):
        y = 0
        for msg in self.messageList:
            screen.blit(msg.surface, (17,screen.get_height() - msg.surface.get_height() - y - 5))
            y += msg.surface.get_height()
            msg.update(self)
            
    def updateTriggers(self):
        # update triggers
        primObjComplete = True
        for tg in self.triggerList:
            tg.update(self)
            if not tg.completed:
                primObjComplete = False
                
        return primObjComplete
    
    def gameLoop(self):
        dt = self.clock.tick(30)
        self.timeTotal += dt
        
        # display the FPS
        if dt > 0: 
            self.fpstext = self.defaultfont.render("FPS: " + str(float(int(10000.0 / dt)) / 10), 1, (0, 250, 0))
            
        if self.gameState == self.GAMESTATE_RUNNING:
            # do physics
            if pygame.time.get_ticks() - self.lastTick > 33:
                self.physics.updatePhysics(self)
                self.lastTick = pygame.time.get_ticks()
                
            # update all sprites
            for sprite in self.backgroundSpriteGroup:
                sprite.update(self)
            
            for sprite in self.shipSpriteGroup:
                sprite.update(self)
        
            for sprite in self.foregroundSpriteGroup:
                sprite.update(self)

            if self.updateTriggers():
                # player completed all primary objectives - mission should end with a victory status now
                self.gameState = self.GAMESTATE_GAMEOVER
                self.menuManager.menu_state_parse(Menu.MENU_MAIN)
                
            if not self.playerShip in self.shipSpriteGroup:
                # player ship died - game over :(
                self.gameState = self.GAMESTATE_GAMEOVER
                self.menuManager.menu_state_parse(Menu.MENU_MAIN)
        
        elif self.gameState == self.GAMESTATE_GAMEOVER:
            for sprite in self.foregroundSpriteGroup:
                sprite.update(self)
            
            self.updateTriggers()
                
        
        if self.gameState != self.GAMESTATE_NONE:       
        
            maxrect = Rect(0,0,0,0)
            for sprite in self.backgroundSpriteGroup: # backgrounds will define the boundaries
                if sprite.rect.left + sprite.rect.width > maxrect.width:
                    maxrect.width = sprite.rect.left + sprite.rect.width
                if sprite.rect.top + sprite.rect.height > maxrect.height:
                    maxrect.height = sprite.rect.top + sprite.rect.height
                
            self.screen_buffer = pygame.Surface((maxrect.width, maxrect.height))
            
        
        
        
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
        
            # TODO display HUD things
            self.screen.blit(self.fpstext, (10,10))
            
            self.screen.blit( 
                self.defaultfont.render("Ammo: " + str(self.playerShip.weapons[self.playerShip.selected_weapon].cur_ammo) + "/" 
                                        + str(self.playerShip.weapons[self.playerShip.selected_weapon].max_ammo), 1, (0, 250, 0)) ,
                (10, 30))
            
            for sprite in self.shipSpriteGroup:
                self.screen.blit( 
                                 self.defaultfont.render(str(sprite.shields) + "/" 
                                        + str(sprite.max_shields), 1, (0, 0, 250)) ,
                                        (sprite.rect.left + render[0], sprite.rect.top + sprite.rect.height + render[1]))
                self.screen.blit(
                                 self.defaultfont.render(str(sprite.health) + "/" 
                                        + str(sprite.max_health), 1, (0, 250, 0)) ,
                                        (sprite.rect.left + render[0], sprite.rect.top + sprite.rect.height + render[1] + 20))
        
        
            self.HUD.draw(self.screen)
            
            self.displayObjectives(self.screen)
            
            self.displayMessages(self.screen)
            
            if self.gameState == self.GAMESTATE_GAMEOVER:
                if self.updateTriggers():
                    text_surf = self.largefont.render("MISSION COMPLETE", 1, (0, 255, 0))
                    self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
                else:
                    text_surf = self.largefont.render("MISSION FAILED", 1, (255, 0, 0))
                    self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
        
        return True
    
    
def Test():
    pygame.init()
    font = pygame.font.Font(None, 20)
    parsed = Utils.parse("Blahblahblahwakkawakkawakka dont do it in the middle of a word!", 100, font)
    for p in parsed:
        print p    
#the main entry point for the program
app = SpaceDominationMain()
app.run()
#Test()
