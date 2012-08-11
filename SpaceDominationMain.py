'''
Created on Apr 28, 2012

@author: Jami

Space Domination

Coded by Jami Couch of PixelNetworks.com

Code and assets released under GPL3.0
Special thanks to Aaron Clifford of EgoAnt.com who produced some of the ship sprites used here.
'''

from AIShip import AIShip, StationShip
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
from xml.sax.xmlreader import AttributesImpl
import Menu
import Utils
import os
import pygame
import pygame.gfxdraw
import random
import sys

VERSION = "0.2"
SPLASH_TIME = 5000
STATE_LOSE_FOCUS = 2
STATE_GAIN_FOCUS = 6


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
    
    # Profile stuff
    profiles = None
    currentProfile = None
    
    HUD = None
    
    def __init__(self):
        '''
        Constructor
        '''
        # before anything else, load the profiles
        self.profiles = ProfileXMLParser().loadProfiles(os.path.join('assets','profiles.xml'))
        for profile in self.profiles:
            if profile['active']:
                self.currentProfile = profile
                break
        
        #initialize managers
        pygame.init()
        random.seed()
        
        try:
            if 'width' in self.currentProfile:
                self.currentProfile['width'] = int(self.currentProfile['width'])
            else:
                self.currentProfile['width'] = 1024
            
            if 'height' in self.currentProfile:
                self.currentProfile['height'] = int(self.currentProfile['height'])
            else:
                self.currentProfile['height'] = 768
                
            self.window = pygame.display.set_mode((self.currentProfile['width'],self.currentProfile['height']))
        except ValueError, msg:
            print "Error in profile height/width: %s" % msg
            self.window = pygame.display.set_mode((1024, 768))
        
        pygame.display.set_caption("Space Domination (version %s) by Jami Couch" % VERSION)
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
        
        # load & display splash screen
        self.showSplash()
        splashTime = pygame.time.get_ticks()
        
        # show the splash for up to 5 seconds or until a key is pressed
        event = None
        keypress = False
        while (not keypress) and pygame.time.get_ticks() < splashTime + SPLASH_TIME:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keypress = True
        
        # remove the splash screen
        self.removeSplash()
        
        # load the mission list
        self.missionList = self.loadMissionList()
        
        # load the menus
        self.menuManager = MenuManager(self.screen, self)
        
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
                            self.pause_game()
                    # movement
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
                    # weapon swapping
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        wp = event.key - pygame.K_1
                        if len(self.playerShip.weapons) >= wp + 1:
                            self.playerShip.selected_weapon = wp
                    
                elif event.type == KEYUP:
                    # movement
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
                
                elif event.type == pygame.ACTIVEEVENT:
                    if event.state == STATE_LOSE_FOCUS:
                        if self.gameState == self.GAMESTATE_RUNNING:
                            self.pause_game()
                        
                        
                elif self.menuManager.is_active() and (event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP):
                    if self.menuManager.is_active():
                        self.menuManager.update(event)
                        if self.menuManager.selectedMenu == -1 and self.gameState == self.GAMESTATE_PAUSED: self.gameState = self.GAMESTATE_RUNNING
                        
                
                '''elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.setKey("fire", 1)
                    print event.button
                
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.setKey("fire", 0)'''

            
            # clear the background (blit a blank screen) then draw everything in the background then the sprite groups then the foreground group
            self.screen.blit(self.background, (0,0))
            
            # game loop
            self.gameLoop()
            if self.gameState == self.GAMESTATE_NONE:
                #drawSurf = pygame.transform.scale(self.menuBackground, self.screen.get_size())
                self.screen.blit(self.menuBackground, ((self.screen.get_width() - self.menuBackground.get_width()) * 0.5, (self.screen.get_height() - self.menuBackground.get_height()) * 0.5))
            if self.menuManager.is_active(): self.menuManager.draw()
            pygame.display.flip()
        
        return
    
    def pause_game(self):
        self.gameState = self.GAMESTATE_PAUSED
        self.menuManager.menu_state_parse(Menu.MENU_PAUSE)
    
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
        #self.rootSprite = pygame.sprite.OrderedUpdates()
        self.shipSpriteGroup = OrderedUpdatesRect()
        self.backgroundSpriteGroup = OrderedUpdatesRect() #pygame.sprite.OrderedUpdates()
        self.foregroundSpriteGroup = OrderedUpdatesRect() #pygame.sprite.OrderedUpdates()
        self.physics = Physics()
        self.messageList = []
        
        #convert spawns to player or enemy
        for spawn in mission.spawnList:
            
            if spawn.type == 'player': # this is the player ship
                tp = PShip()
                tp.file = "redfighter0jv.png" # todo - obviously we should load this in a player-specific manner
                tp.weapons.append(0)
                tempShip = PlayerShip(proto = self.shipList[0], context = self )
                self.playerShip = tempShip
                self.linkTriggers(spawn, tempShip)
            else:
                if spawn.id >= 0 and spawn.id < len(self.shipList):
                    tempShip = AIShip(spawn.x, spawn.y, spawn.r, proto = self.shipList[spawn.id], context = self)
                    
                    self.linkTriggers(spawn, tempShip)
                elif spawn.id == -1:
                    tempShip = StationShip(spawn.x, spawn.y, spawn.r, proto = spawn.proto, context = self)
                    for pt in spawn.hard_points:
                        if pt.id >= 0 and pt.id < len(self.shipList):
                            hpt = AIShip(spawn.x + pt.x, spawn.y + pt.y, spawn.r + pt.r, proto = self.shipList[pt.id], parent = tempShip, context = self)         
                            tempShip.hard_points.append(hpt)
                    
                    self.linkTriggers(spawn, tempShip)
                
            self.shipSpriteGroup.add(tempShip)
            self.foregroundSpriteGroup.add(tempShip.hard_points)
            self.physics.addChild(tempShip)
            tempShip.set_position(spawn.x, spawn.y)
            tempShip.set_rotation(spawn.r)
            tempShip.tag = spawn.tag
            
            
        # first, set up any auto-backgrounds
        if mission.background_style == 'tiled':
            # set up a tiled background using background_file and width, height
            x = 0
            y = 0
            mission.background_image, dfrect = Utils.load_image(mission.background_file)
            
        
        #convert bglist to backgrounds
        for bg in mission.backgroundList:
            tempBg = pygame.sprite.Sprite()
            tempBg.image, tempBg.rect = Utils.load_image(bg.filename)
            tempBg.rect.topleft = (bg.x, bg.y)
            self.backgroundSpriteGroup.add(tempBg)
        
    
    def linkTriggers(self, spawn, ship):
        for tg in self.triggerList:
            if tg.parent == spawn:
                tg.parent = ship
            
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
            
            # use the given mission width/height and the backgrounds to determine the boundaries
            maxrect = Rect(0,0,self.currentMission.width,self.currentMission.height)
            for sprite in self.backgroundSpriteGroup: # backgrounds will define the boundaries
                if sprite.rect.left + sprite.rect.width > maxrect.width:
                    maxrect.width = sprite.rect.left + sprite.rect.width
                if sprite.rect.top + sprite.rect.height > maxrect.height:
                    maxrect.height = sprite.rect.top + sprite.rect.height
                
            # now render to the screen using the playerShip to decide on coords
            render = (-1 * self.playerShip.rect.center[0] + (self.screen.get_width() * 0.5), -1 * self.playerShip.rect.center[1] + (self.screen.get_height() * 0.5))
            if render[0] > 0: render = (0, render[1])
            if render[1] > 0: render = (render[0], 0)
            if render[0] < -1 * maxrect.width + self.screen.get_width(): render = (-1 * maxrect.width + self.screen.get_width(), render[1])
            if render[1] < -1 * maxrect.height + self.screen.get_height(): render = (render[0], -1 * maxrect.height + self.screen.get_height())
            
            # draw a tiled background if necessary
            if self.currentMission and self.currentMission.background_style == 'tiled' and self.currentMission.background_image:
                # we will always assume that 0,0 is the starting point for the tiling
                bgimg = self.currentMission.background_image
                # set the offset to start at the closest tiling position to the top/left of the current area
                offset = [-1 * render[0], -1 * render[1]]
                offset[0] = int(offset[0] / bgimg.get_width()) * bgimg.get_width()
                offset[1] = int(offset[1] / bgimg.get_height()) * bgimg.get_height()
                start = [offset[0], offset[1]]
                end = [-1 * render[0] + self.screen.get_width(), -1 * render[1] + self.screen.get_height()]
                # render the tiles until off the screen
                while offset[0] < end[0] and offset[1] < end[1]:
                    self.screen.blit(bgimg, (offset[0] + render[0], offset[1] + render[1]))
                    offset[0] += bgimg.get_width()
                    if offset[0] >= end[0]:
                        offset[0] = start[0]
                        offset[1] += bgimg.get_height()
                
            # now draw the sprites
            drawrect = pygame.rect.Rect(-1 * render[0], -1 * render[1], self.screen.get_width(), self.screen.get_height())
            self.backgroundSpriteGroup.draw(self.screen, drawrect, render)
            self.shipSpriteGroup.draw(self.screen, drawrect, render)
            self.foregroundSpriteGroup.draw(self.screen, drawrect, render)
        
        
            # TODO display HUD things
            self.screen.blit(self.fpstext, (10,10))
            
            for sprite in self.shipSpriteGroup:
                # TODO change these to bars (open/filled rect)
                self.screen.blit( 
                                 self.defaultfont.render(str(sprite.shields) + "/" 
                                        + str(sprite.max_shields), 1, (0, 0, 250)) ,
                                        (sprite.rect.left + render[0], sprite.rect.top + sprite.rect.height + render[1]))
                self.screen.blit(
                                 self.defaultfont.render(str(sprite.health) + "/" 
                                        + str(sprite.max_health), 1, (0, 250, 0)) ,
                                        (sprite.rect.left + render[0], sprite.rect.top + sprite.rect.height + render[1] + 20))
                
                if isinstance(sprite, StationShip):
                    for hp in sprite.hard_points:
                        self.screen.blit(self.defaultfont.render("%i/%i" % (int(hp.health), int(hp.max_health)), 1, (0, 250, 0)),
                                         (hp.rect.left + render[0], hp.rect.top + hp.rect.height + render[1]))
                                                                 
                #if not sprite == self.playerShip:
                #    pygame.gfxdraw.box(self.screen, pygame.rect.Rect(sprite.waypoint[0] - 5 + render[0], sprite.waypoint[1] - 5 + render[1], 10, 10), (51, 102, 255))
        
        
            self.HUD.draw(self.screen, self, render)
            
            
            if self.gameState == self.GAMESTATE_GAMEOVER:
                if self.updateTriggers():
                    text_surf = self.largefont.render("MISSION COMPLETE", 1, (0, 255, 0))
                    self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
                else:
                    text_surf = self.largefont.render("MISSION FAILED", 1, (255, 0, 0))
                    self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
        
        return True

class OrderedUpdatesRect(pygame.sprite.OrderedUpdates):
    '''
    extension of pygame.sprite.OrderedUpdates with a draw function that 
    accepts a rect defining the "screen" and an offset for where to draw the 
    sprites on the surface
    
    '''  
    
    def draw(self, surface, rect = None, offset = None):
        '''draw only sprites contained in rect to surface at offset
        
        OrderedUpdatesRect.draw(surface, rect, offset) returns None
        
        @param surface     target for rendering
        @param rect        only sprites that collide with this rect will be rendered
        @param offset      sprites will be rendered with this offset
        '''
        for spt in self.sprites():
            if not rect or spt.rect.colliderect(rect):
                if offset:
                    self.spritedict[spt] = surface.blit(spt.image, (spt.rect.left + offset[0], spt.rect.top + offset[1]))
                else:
                    self.spritedict[spt] = surface.blit(spt.image, spt.rect)
                    
class ProfileXMLParser(handler.ContentHandler):
    '''load the profiles from a specified xml file'''
    profileList = None
    defaultID = 0
    
    def __init__(self):
        handler.ContentHandler.__init__(self)
        self.profileList = []
    
    def loadProfiles(self, filename = None):
        '''load the profiles from @param filename (defaults to assets/profiles.xml)'''
        if not filename:
            filename = os.path.join("assets","profiles.xml")
        parser = make_parser()
        parser.setContentHandler(self)
        parser.parse(filename)
        return self.profileList
        
    
    def startElement(self, name, attrs):
        if name == "profiles":
            self.profileList = []
            self.defaultID = int(attrs.get('default',0))
        elif name == "profile":
            keys = attrs.keys()
            profile = {}
            for key in keys:
                profile[key] = attrs.get(key)
            if int(profile['id']) == self.defaultID:
                profile['active'] = True
            self.profileList.append(profile)
    
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass


#the main entry point for the program
if __name__ == "__main__":
    app = SpaceDominationMain()
    app.run()
