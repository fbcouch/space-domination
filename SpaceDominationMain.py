'''
Created on Apr 28, 2012

@author: Jami

Space Domination

Coded by Jami Couch of PixelNetworks.com

Code and assets released under GPL3.0
'''

from AIShip import AIShip, StationShip
from Menu import SpaceDominationGUI
from Mission import *
from Particle import Particle
from Physics import *
from PhysicsEntity import PhysicsEntity
from PlayerShip import PlayerShip
from Ship import Ship, PShip, Weapon, ShipListXMLParser
from Utils import load_sprite_sheet
from Weapon import WeaponListXMLParser
from campaign import CampaignManager
from consts import MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, VERSION, SPLASH_TIME, \
    STATE_LOSE_FOCUS, FRAMERATE
from gui.basicmenu import BasicMenu, BasicTextButton
from gui.gui import GUI
from hud import HUD
from profile import Profile
from pygame.locals import *
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl
import Menu
import Utils
import consts
import os
import profile
import pygame
import pygame.gfxdraw
import random
import sys
import xml.sax

class SpaceDominationMain(object):
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
    medfont = None
    
    rootSprite = None
    
    shipSpriteGroup = None
    destroyedSpriteGroup = None
    backgroundSpriteGroup = None
    triggerList = None
    foregroundSpriteGroup = None
    elapsedTime = 0.0
    messageList = None
    
    # Profile stuff
    profiles = None
    currentProfile = None
    
    HUD = None
    
    # Campaign manager
    campaignMgr = None
    
    def __init__(self):
        '''
        Constructor
        '''
        # before anything else, load the profiles
        self.profiles = ProfileXMLParser().loadProfiles(os.path.join('assets','profiles.xml'))
        for p in self.profiles:
            if 'active' in p and p['active']:
                self.currentProfile = p
                break
        
        if not self.currentProfile:
            if len(self.profiles) > 0:
                self.currentProfile = self.profiles[0]
            else:
                self.setActiveProfile(profile.create_fresh_profile(id = 0))
                self.saveProfiles()
        
        #initialize managers
        pygame.init()
        random.seed()
        
        self.createDisplay()
        
        
        Utils.load_common_assets()
        
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
            self.medfont = pygame.font.Font(None, 30)
        
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
        
        # load the Campaign mangager
        self.campaignMgr = CampaignManager(self)
        
        # load the menus
        #self.menuManager = MenuManager(self.screen, self)
        self.menuManager = SpaceDominationGUI(self)
        
        
        self.gameState = SpaceDominationMain.GAMESTATE_NONE
        self.menuBackground = load_image("background.PNG")[0]
        #self.menuManager.menu_state_parse(Menu.MENU_MAIN)
        self.menuManager.set_active(True)
        self.menuManager.main_menu_click()
        # TODO: show the menu
        # eventually the menu will lead to...
        #self.gameState = SpaceDominationMain.GAMESTATE_RUNNING
        #self.currentMission = self.loadMission("mission01.xml")
        #self.buildMission(self.currentMission)
    
    def run(self):
        rect_list = []
        while True:
            # handle input
            events = pygame.event.get()
            
            for event in events:
                if event.type == QUIT:
                    sys.exit(0)
                elif self.menuManager.is_active():
                    self.menuManager.update(event)
                
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
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
        self.menuManager.pause_menu_click()
        
    def unpause_game(self):
        self.gameState = self.GAMESTATE_RUNNING
        self.menuManager.close()
        
    def quit_mission(self):
        self.gameState = self.GAMESTATE_GAMEOVER
        self.menuManager.main_menu_click()
    
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
    
    def startMission(self, mission):
        if isinstance(mission, Mission):
            self.currentMission = mission
        else:
            self.currentMission = self.loadMission(mission[0])
        self.buildMission(self.currentMission)
        self.pause_game()
    
    def buildMission(self, mission):
        self.elapsedTime = 0.0
        #add the trigger list
        self.triggerList = mission.triggerList[:]
        #self.rootSprite = pygame.sprite.OrderedUpdates()
        self.shipSpriteGroup = OrderedUpdatesRect()
        self.destroyedSpriteGroup = OrderedUpdatesRect()
        self.backgroundSpriteGroup = OrderedUpdatesRect() #pygame.sprite.OrderedUpdates()
        self.foregroundSpriteGroup = OrderedUpdatesRect() #pygame.sprite.OrderedUpdates()
        self.physics = Physics()
        self.messageList = []
        for key in self.keys: 
            self.setKey(key, 0)
        
        #convert spawns to player or enemy
        for spawn in mission.spawnList:
            
            if spawn.type == 'player': # this is the player ship
                tp = self.shipList[0]
                for proto in self.shipList:
                    if 'ship' in self.currentProfile and proto.id == int(self.currentProfile['ship']):
                        tp = proto
                tempShip = PlayerShip(proto = tp, context = self)
                tempShip.team = spawn.team
                self.playerShip = tempShip
                self.linkTriggers(spawn, tempShip)
            else:
                if spawn.id >= 0 and spawn.id < len(self.shipList):
                    if self.shipList[spawn.id].hard_points:
                        tempShip = StationShip(spawn.x, spawn.y, proto = self.shipList[spawn.id], context = self)
                        for pt in self.shipList[spawn.id].hard_points:
                            hpt = AIShip(spawn.x + pt['x'], spawn.y + pt['y'], spawn.r + pt['rot'], proto = self.shipList[pt['id']], parent = tempShip, context = self)
                            hpt.team = tempShip.team
                            tempShip.hard_points.append(hpt)
                    else:
                        tempShip = AIShip(spawn.x, spawn.y, spawn.r, proto = self.shipList[spawn.id], context = self)
                    tempShip.team = spawn.team
                    
                    self.linkTriggers(spawn, tempShip)
                    
                    
                elif spawn.id == -1:
                    if spawn.hard_points:
                        tempShip = StationShip(spawn.x, spawn.y, spawn.r, proto = spawn.proto, context = self)
                    
                        for pt in spawn.hard_points:
                            if pt.id >= 0 and pt.id < len(self.shipList):
                                hpt = AIShip(spawn.x + pt.x, spawn.y + pt.y, spawn.r + pt.r, proto = self.shipList[pt.id], parent = tempShip, context = self)    
                                hpt.team = tempShip.team     
                                tempShip.hard_points.append(hpt)
                    else:
                        tempShip = AIShip(spawn.x, spawn.y, spawn.r, proto = spawn.proto, context = self)
                        
                    tempShip.team = spawn.team
                    self.linkTriggers(spawn, tempShip)
                    
            if spawn.squad:
                spawn.squad.append(tempShip)
                tempShip.squad = spawn.squad
            self.shipSpriteGroup.add(tempShip)
            self.foregroundSpriteGroup.add(tempShip.hard_points)
            self.physics.addChild(tempShip)
            tempShip.set_position(spawn.x, spawn.y)
            tempShip.set_rotation(spawn.r)
            tempShip.tag = spawn.tag
            tempShip.spawn = spawn
            tempShip.apply_upgrade(spawn.upgrade)
            
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
            
        self.updateTriggers()
    
    def endMission(self):
        
        self.gameState = self.GAMESTATE_GAMEOVER
        
        #self.menuManager.main_menu_click()
        
        # put together the results for the mission results menu
        destroyedSpawns = self.currentMission.get_losses(self.destroyedSpriteGroup)
        destroyedLabels = {'ally': {}, 'enemy': {}}
        
        for sp in destroyedSpawns:
            if sp.team == Ship.TEAM_DEFAULT_FRIENDLY:
                update = destroyedLabels['ally']
            else:
                update = destroyedLabels['enemy']
            
            if not sp.id in update.keys():
                # create a new entry
                lb = "Unknown"
                img = None
                if sp.id == -1 and sp.type == "player":
                    lb = self.shipList[int(self.currentProfile['ship'])].name
                    img = self.shipList[int(self.currentProfile['ship'])].image
                elif sp.id >= 0 and sp.id < len(self.shipList):
                    lb = self.shipList[sp.id].name
                    img = self.shipList[sp.id].image
                update[sp.id] = {'num': 1, 'label': lb, 'image': img}
            else:
                # update the existing entry
                update[sp.id]['num'] += 1
        
        results = {'win': self.updateTriggers(), 'labels': destroyedLabels, 'spawns': destroyedSpawns, 'ships': self.destroyedSpriteGroup}
        
        if self.currentMission.isCampaignMission:
            self.campaignMgr.mission_ended(results, self.currentMission)
        self.menuManager.mission_results_show(results, self.currentMission)
        return results['win']
        
    def linkTriggers(self, spawn, ship):
        for tg in self.triggerList:
            if tg.parent == spawn:
                tg.parent = ship
            
    def updateTriggers(self):
        # update triggers
        primObjComplete = True
        for tg in self.triggerList:
            tg.update(self)
            if not tg.completed and tg.type.count("objective-primary") > 0:
                primObjComplete = False
                
        return primObjComplete
    
    def gameLoop(self):
        dt = self.clock.tick(consts.FRAMERATE)
        self.timeTotal += dt
        
        # display the FPS
        if dt > 0: 
            self.fpstext = self.defaultfont.render("FPS: " + str(float(int(10000.0 / dt)) / 10), 1, (0, 250, 0))
            
        if self.gameState == self.GAMESTATE_RUNNING:
            # do physics
            if self.lastTick == 0: self.lastTick = pygame.time.get_ticks()
            #if pygame.time.get_ticks() - self.lastTick > 33:
            #    self.physics.updatePhysics(self)
            #    self.lastTick = pygame.time.get_ticks()
            timestep = float(dt) * consts.GAMESPEED * 0.001
            
            self.elapsedTime += dt
            
            self.physics.updatePhysics(self, timestep)
            
            vel = Vec2(0,0)
            vel.setXY(*self.playerShip.velocity)
            #print "Ship: %f / Vel: %f (%f, %f) / timestep: %f" % (self.playerShip.get_rotation(), vel.theta, self.playerShip.velocity[0], self.playerShip.velocity[1], timestep)
                
            # update all sprites
            for sprite in self.backgroundSpriteGroup:
                sprite.update(self)
            
            for sprite in self.shipSpriteGroup:
                sprite.update(self, timestep)
        
            for sprite in self.foregroundSpriteGroup:
                sprite.update(self, timestep)

            if self.updateTriggers():
                # player completed all primary objectives - mission should end with a victory status now
                self.endMission()
                
            if not self.playerShip in self.shipSpriteGroup:
                # player ship died - game over :(
                #self.gameState = self.GAMESTATE_GAMEOVER
                #self.menuManager.main_menu_click()
                self.endMission()
            
            if self.gameState == self.GAMESTATE_GAMEOVER:
                # TODO the game is ending, save the profile stats
                if not 'shots-fired' in self.currentProfile:
                    self.currentProfile['shots-fired'] = 0
                self.currentProfile['shots-fired'] = int(self.currentProfile['shots-fired']) + int(self.playerShip.stats['shots-fired'])
                
                if not 'shots-hit' in self.currentProfile:
                    self.currentProfile['shots-hit'] = 0
                self.currentProfile['shots-hit'] = int(self.currentProfile['shots-hit']) + int(self.playerShip.stats['shots-hit'])
                
                if not 'damage-dealt' in self.currentProfile:
                    self.currentProfile['damage-dealt'] = 0
                self.currentProfile['damage-dealt'] = int(self.currentProfile['damage-dealt']) + int(self.playerShip.stats['damage-dealt'])
                
                if not 'damage-taken' in self.currentProfile:
                    self.currentProfile['damage-taken'] = 0
                self.currentProfile['damage-taken'] = int(self.currentProfile['damage-taken']) + int(self.playerShip.stats['damage-taken'])
                
                if not 'kills' in self.currentProfile:
                    self.currentProfile['kills'] = 0
                self.currentProfile['kills'] = int(self.currentProfile['kills']) + int(self.playerShip.stats['kills'])
                
                death = 0
                if not self.playerShip in self.shipSpriteGroup:
                    death = 1
                if not 'deaths' in self.currentProfile:
                    self.currentProfile['deaths'] = 0
                self.currentProfile['deaths'] = int(self.currentProfile['deaths']) + death
                
                self.saveProfiles()
        
        elif self.gameState == self.GAMESTATE_GAMEOVER:
            for sprite in self.foregroundSpriteGroup:
                if isinstance(sprite, Particle): sprite.update(self)
            
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
                # set up parralax
                offset[0] -= (bgimg.get_width() - consts.PARALLAX * render[0] % bgimg.get_width())
                offset[1] -= (bgimg.get_height() - consts.PARALLAX * render[1] % bgimg.get_height())
                #offset[0] = int(offset[0] / bgimg.get_width()) * bgimg.get_width()
                #offset[1] = int(offset[1] / bgimg.get_height()) * bgimg.get_height()
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
            self.screen.blit(self.fpstext, (10,30))
            
            
                
                #if isinstance(sprite, AIShip):
                #    rect = pygame.rect.Rect(0,0,10,10)
                #    rect.center = (sprite.waypoint[0] + render[0], sprite.waypoint[1] + render[1])
                #    pygame.gfxdraw.box(self.screen, rect, (0, 0, 250))
                                                        
        
            self.HUD.draw(self.screen, self, render)
                
            
            #if self.gameState == self.GAMESTATE_GAMEOVER:
            #    if self.updateTriggers():
            #        text_surf = self.largefont.render("MISSION COMPLETE", 1, (0, 255, 0))
            #        self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
            #    else:
            #        text_surf = self.largefont.render("MISSION FAILED", 1, (255, 0, 0))
            #        self.screen.blit( text_surf, (self.screen.get_width() * 0.5 - text_surf.get_width() * 0.5, 100))
            
        return True
    
    def createDisplay(self):
        '''creates a display from the current profile settings'''
        try:
            if 'width' in self.currentProfile and int(self.currentProfile['width']) >= MIN_WINDOW_WIDTH:
                self.currentProfile['width'] = int(self.currentProfile['width'])
            else:
                self.currentProfile['width'] = MIN_WINDOW_WIDTH
            
            if 'height' in self.currentProfile and int(self.currentProfile['height']) >= MIN_WINDOW_HEIGHT:
                self.currentProfile['height'] = int(self.currentProfile['height'])
            else:
                self.currentProfile['height'] = MIN_WINDOW_HEIGHT
                
            if not 'fullscreen' in self.currentProfile:
                self.currentProfile['fullscreen'] = 0
            flags = 0
            if int(self.currentProfile['fullscreen']):
                flags = pygame.FULLSCREEN
            self.window = pygame.display.set_mode((self.currentProfile['width'],self.currentProfile['height']), flags)
        except pygame.error, msg:
            print "Error in profile video mode: %s" % msg
            self.window = pygame.display.set_mode((1024, 768))
    
    def saveProfiles(self, filename = None):
        '''saves the profiles to filename (default asstes/profiles.xml)'''
        if not filename:
            filename = os.path.join('assets', 'profiles.xml')
        xml_file = open(filename, "w")
        xmlgen = XMLGenerator(xml_file, 'UTF-8')
        xmlgen.startDocument()
        xmlgen.startElement('profilelist', {'default': str(self.currentProfile['id'])})
        xml_file.write('\n')
        for profile in self.profiles:
            keys = {}
            for key in profile:
                if not key == 'active':
                    keys[key] = str(profile[key])
            xml_file.write('\t')
            xmlgen.startElement('profile', keys)
            xmlgen.endElement('profile')
            xml_file.write('\n')
        xmlgen.endElement('profilelist')
        xmlgen.endDocument()
        xml_file.write('\n')
        xml_file.close()
        
        self.createDisplay()
        
    def setActiveProfile(self, profile):
        if not profile in self.profiles:
            self.profiles.append(profile)
        
        self.currentProfile = profile
    
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
            if isinstance(spt, PhysicsEntity) and not spt.active:
                continue
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
        if name == "profilelist":
            self.profileList = []
            self.defaultID = int(attrs.get('default',0))
        elif name == "profile":
            self.profileList.append(profile.create_profile_from_attrs(attrs, self.defaultID))
    
    def endElement(self, name):
        pass
    
    def characters(self, content):
        pass

        
    
#the main entry point for the program
def test_gui():
    pygame.init()
    window = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Testing GUI")
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    font = None
    if pygame.font:
        font = pygame.font.Font(None, 20)
    
    gui = GUI(None)
    gui.set_active(True)
    menu = BasicMenu(gui, h_pad=10, v_pad=10)
    gui.add_child(menu)
    menu.set_active(True)
    menu.add_child(BasicTextButton(menu, text = 'Select Mission', select_fxn = menu.mouse_over_callback, callback = gui.generic_click, callback_kwargs = {'target_id': 1}))
    menu.add_child(BasicTextButton(menu, text = 'Exit', select_fxn = menu.mouse_over_callback, callback = gui.exit_click))
    gui.add_child(BasicMenu(gui))
    '''
    frame = Frame(gui)
    gui.add_child(frame)
    frame.set_active(True)
    
    testel = TestElement(frame)
    testel.image = pygame.surface.Surface((100,50))
    testel.image = testel.image.convert()
    testel.image.fill((51, 102, 255))
    testel.rect = testel.image.get_rect()
    testel.rect.topleft = ((window.get_width() - testel.rect.width) * 0.5, (window.get_height() - testel.rect.height) * 0.5)
    '''
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
        
        if gui.is_active(): gui.update(events)
        
        screen.blit(background, (0,0))
        
        if gui.is_active(): gui.draw()
        
        pygame.display.flip()
        

if __name__ == "__main__":
    #test_gui()
    app = SpaceDominationMain()
    app.run()
