'''
Created on Sep 12, 2012

@author: Jami
'''
from AIShip import Squadron
from Mission import Mission, Spawn
from Ship import Ship
from Trigger import CreateTrigger
from Vec2 import Vec2
from gui.basicmenu import BasicImageButton, ImageLabel, BasicTextButton
from gui.gui import Frame
import Utils
import consts
import math
import pygame
import random

DEFAULT_PLANETS = 10
DEFAULT_BOARD_WIDTH = 8
DEFAULT_BOARD_HEIGHT = 8


class CampaignManager(object):
    '''
    CampaignManager will basically handle setting up the current campaign for us and creating the relevant menus, etc
    '''
    campaignList = None
    currentCampaign = None
    
    context = None
    
    display = None

    planetNames = None
    planetFiles = None

    def __init__(self, context = None, campaigns = None, selected = None):
        '''
        Constructor
        '''
        self.context = context
        self.campaignList = campaigns
        
        self.currentCampaign = selected
        
        
        if selected and self.campaignList and selected not in self.campaignList:
            self.campaignList.append(selected)
            
        self.load_planet_info()
        
        if not self.campaignList:
            self.campaignList = []
            self.create_new_random()
        
        if not self.currentCampaign:
            self.currentCampaign = self.campaignList[0]
        
    def load_planet_info(self):
        '''
        TODO load a list of planet names and files that can be randomly assigned
        '''
        # for now, just use the following (over and over again...)
        self.planetNames = ['Kyoukan', 'Pixelia', 'Morbo', 'Arrakan', 'Twili', 'Zerb', 'Blorg', 'Bleep', 'Malthus', 'Hayekia']
        self.planetFiles = ['desert-planet.png', 'earthy-planet.png', 'burnt-planet.png']
            
    def create_new_random(self, planets = DEFAULT_PLANETS, width = DEFAULT_BOARD_WIDTH, height = DEFAULT_BOARD_HEIGHT, **kwargs):
        if planets > width * height:
            planets = width * height
        
        planetList = []
        factions = [{'name': "Red team", 'color': consts.COLOR_RED, 'ai' : None}, {'name': "Blue team", 'color': consts.COLOR_BLUE, 'ai' : None}]
        # don't want to reuse names, so we copy the list 
        names = list(self.planetNames)
        for i in range(0, planets):
            planet = self.create_random_planet(names, self.planetFiles)
            if planet.name in names: names.remove(planet.name)
            
            # now we need to assign the planet to an open board position
            while not planet.boardPosition:
                # generate a random position
                pos = (random.randint(0, width - 1), random.randint(0, height - 1))
                
                # is this position already taken?
                taken = False
                for p in planetList:
                    if p.boardPosition == pos:
                        taken = True
                
                if not taken:
                    planet.boardPosition = pos
            
            #planet.faction = factions[random.randint(0, len(factions) - 1)]    
            #planet.strength = random.randint(1, 3)
            planetList.append(planet)
        
        cp = Campaign()
        cp.planets = planetList
        cp.factions = factions
        
        points = len(cp.planets) / len(cp.factions)
        for f in factions:
            f['ai'] = FactionAI(cp, f)
            f['ai'].planet_upgrade_points = points
        
        cp.init()
        cp.boardSize = (width, height)
        self.campaignList.append(cp)
        return cp
        
    def create_random_planet(self, names = None, files = None):
        '''
        generate a random planet name/file
        '''
        if not names:
            names = self.planetNames
        if not files:
            files = self.planetFiles
        
        if len(names) == 0 and len(files) == 0:
            return Planet()
        elif len(names) == 0:
            return Planet(file = files[random.randint(0, len(files) - 1)])
        elif len(files) == 0:
            return Planet(names[random.randint(0, len(names) - 1)])
        
        return Planet(names[random.randint(0, len(names) - 1)], files[random.randint(0, len(files) - 1)])
    
    def show_display(self, parent):
        self.display = CampaignMenu(parent, campaign = self.currentCampaign, manager = self, ship_list = self.context.shipList, mission_start = self.context.startMission)
        parent.add_child(self.display)
        self.display.set_active(True)

    def mission_ended(self, result, mission):
        
        pass

class FactionAI(object):
    '''
    Handles the AI for a given faction
    '''
    
    campaign = None
    faction = None
    planets = None
    fleets = None
    
    planet_upgrade_points = 0
    fleet_upgrade_points = 0
    
    def __init__(self, campaign, faction):
        self.campaign = campaign
        self.faction = faction
        self.planets = []
        self.fleets = []
    
    def choose_planet(self, available):
        if len(self.planets) == 0:
            # if we don't have one, choose one randomly
            planet = available[random.randint(0, len(available) - 1)]
            self.planets.append(planet)
            planet.faction = self.faction
            return planet
        elif len(available) == 1:
            self.planets.append(available[0])
            available[0].faction = self.faction
            return available[0]
        else:
            # choose the nearest planet
            near = None
            ndist = 0
            for p in available:
                if not near:
                    near = p
                for l in self.planets:
                    dist = (p.boardPosition[0] - l.boardPosition[0]) ** 2 + (p.boardPosition[1] - l.boardPosition[1]) ** 2
                    if not l is p and (ndist == 0 or dist < ndist):
                        near = p
                        ndist = dist
            self.planets.append(near)
            near.faction = self.faction
            return near
    
    def do_turn(self):
        # TODO spend planet upgrade points
        while self.planet_upgrade_points > 0:
            self.spend_planet_upgrade_point()
            
        # TODO spend fleet upgrade points
        self.spend_fleet_upgrade_point()    
        
        # TODO move fleets around and select a battle
        b = None
        for f in self.fleets:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            if f.board_position[0] + dx < 0:
                dx = random.randint(0, 1)
            elif f.board_position[0] + dx >= self.campaign.boardSize[0]:
                dx = random.randint(-1, 0)
            
            if f.board_position[1] + dy < 0:
                dy = random.randint(0, 1)
            elif f.board_position[1] + dy >= self.campaign.boardSize[1]:
                dy = random.randint(-1, 0)
                
            occupy = self.campaign.occupied_by((f.board_position[0] + dx, f.board_position[1] + dy))
             
            if (isinstance(occupy, Fleet) and not occupy in self.fleets) or (isinstance(occupy, Planet) and not occupy in self.planets):
                if not b:
                    b = Battle()
                    b.start = f.board_position
                    b.end = (f.board_position[0] + dx, f.board_position[1] + dy)
            else:
                f.board_position = (f.board_position[0] + dx, f.board_position[1] + dy)
        return b
    
    
    def spend_planet_upgrade_point(self):
        if self.planet_upgrade_points > 0:
            self.planets[random.randint(0, len(self.planets) - 1)].strength += 1
            self.planet_upgrade_points -= 1
    
    def spend_fleet_upgrade_point(self):
        pass
    
    def place_fleet(self):
        ft = Fleet()
        self.fleets.append(ft)
        self.campaign.fleets.append(ft)
        ft.faction = self.faction
        ft.board_position = self.planets[random.randint(0, len(self.planets) - 1)].boardPosition
        for i in range(0, 6):
            ft.ship_id_list.append(3)
        
    
class Campaign(object):
    '''
    Contains the status of a campaign...this theoretically should be saved/loaded from files
    '''
    planets = None
    boardSize = None
    factions = None
    fleets = None
    battles = None
    
    def __init__(self):
        self.planets = []
        self.boardSize = (0,0)
        self.factions = []
        self.fleets = []
        self.battles = []
        
        
    def init(self):
        '''
        initializes the campaign
        '''
        self.faction_choose_planets()
        
        points = self.factions[0]['ai'].planet_upgrade_points
        i = 0
        while i < points:
            for f in self.factions:
                f['ai'].spend_planet_upgrade_point()
            i += 1
        
        fleets = float(len(self.planets)) / consts.PLANETS_PER_FLEET
        if fleets - int(fleets) >= 0.5:
            fleets = int(fleets) + 1
        else:
            fleets = int(fleets)
        
        i = 0
        while i < fleets:
            for f in self.factions:
                f['ai'].place_fleet()
            i += 1
            
        
        
    def faction_choose_planets(self):
        remaining_planets = self.planets[:]
        for i in range(len(self.planets)):
            p = self.factions[i % len(self.factions)]['ai'].choose_planet(remaining_planets)
            p.strength = 1
            if p in remaining_planets: remaining_planets.remove(p)
            
    def occupied_by(self, pos):        
        '''returns the planet or fleet occupying this space'''
        
        for p in self.planets:
            if p.boardPosition == pos:
                return p
        
        for f in self.fleets:
            if f.board_position == pos:
                return f
        
    def do_turn(self, **kwargs):
        self.battles = []
        for f in self.factions:
            f['ai'].planet_upgrade_points += len(f['ai'].planets)
            f['ai'].fleet_upgrade_points += len(f['ai'].planets)
            
            b = f['ai'].do_turn()
            if b:
                self.battles.append(b)
                
        return self.battles

class Battle(object):
    faction = None # the faction owning the battle
    start = None # the location of the fleet attacking
    end = None # the destination

class Fleet(object):
    faction = None
    board_position = None
    armor_level = 0
    weapon_level = 0
    ship_id_list = None
    
    def __init__(self):
        self.ship_id_list = []

class Planet(object):
    '''
    Within the context of a campaign, there will be planets with some attributes such as defense level, etc
    '''
    file = None
    sprite = None
    boardPosition = None
    name = None
    faction = None
    strength = 0
    
    mission = None
    
    def __init__(self, name = "default", imgfile = None, pos = None):
        '''
        Constructor
        '''
        self.name = name
        self.file = imgfile
        self.boardPosition = pos
        self.sprite = pygame.sprite.Sprite()
        if self.file:
            self.set_file(self.file)
        
    def set_file(self, imgfile):
        self.file = imgfile
        try:
            self.sprite.image, self.sprite.rect = Utils.load_image(self.file, -1)
        except SystemExit, e:
            print "Class Planet: could not load image"
        
    def get_mission(self, ship_list):
        if not self.mission:
            # generate a mission
            self.mission = self.create_mission(ship_list)
            
        for tg in self.mission.triggerList:
            tg.completed = False
            
        self.mission.triggerList[len(self.mission.triggerList) - 1].parent = self.mission.spawnList[0]
        return self.mission
    
    def create_mission(self, ship_list):
        mission = Mission()
        mission.background_file = 'default_background.png'
        mission.background_style = 'tiled'
        mission.width = 5000
        mission.height = 5000
        mission.isCampaignMission = True
        
        squad = Squadron()
        
        proto = ship_list[3]
        # add a player spawn randomly
        sp = Spawn()
        sp.id = -1
        sp.type = "player"
        sp.team = Ship.TEAM_DEFAULT_FRIENDLY
        sp.x = random.randint(mission.width * 0.25, mission.width * 0.75)
        sp.y = random.randint(mission.height * 0.25, mission.height * 0.75)
        sp.r = random.randint(0, 360)
        sp.tag = "self"
        if not mission.spawnList: mission.spawnList = []
        mission.spawnList.append(sp)
        
        squad.squad_target = (sp.x, sp.y)
        squad.angle = sp.r
        #sp.squad = squad
        
        sp = Spawn()
        sp.id = 0
        sp.type = "friendly"
        sp.team = Ship.TEAM_DEFAULT_FRIENDLY
        sp.tag = "ally"
        offset = Vec2(0, 0)
        offset.setXY(squad.formation[1][0], squad.formation[1][1])
        offset.theta += squad.angle
        offset = offset.getXY()
        
        sp.x = squad.squad_target[0] + offset[0] 
        sp.y = squad.squad_target[1] + offset[1]
        sp.r = squad.angle
        mission.spawnList.append(sp)
        
        #sp.squad = squad
        
        
        for i in range(0, self.strength * 3):
            if i % 3 == 0:
                squad = Squadron()
                squad.angle = random.randint(0, 360)
                conflicts = True
                while conflicts:
                    x = random.randint(0, mission.width)
                    y = random.randint(0, mission.height)
                    conflicts = False
                    for s in mission.spawnList:
                        if s.x**2 + s.y**2 - x**2 + y**2 < 1000**2:
                            conflicts = True
                squad.squad_target = (x, y)
            else:
                offset = Vec2(0, 0)
                offset.setXY(squad.formation[i % 3][0], squad.formation[i % 3][1])
                offset.theta += squad.angle
                offset = offset.getXY()
                
                x = squad.squad_target[0] + offset[0] 
                y = squad.squad_target[1] + offset[1]
            sp = Spawn()
        
            sp.id = 3
            sp.proto = proto
            sp.team = Ship.TEAM_DEFAULT_ENEMY
            
            sp.squad = squad
            sp.x = x
            sp.y = y 
            sp.r = squad.angle
            sp.tag = 'primary'
                
            if not mission.spawnList: mission.spawnList = []
            mission.spawnList.append(sp)
            
        if not mission.triggerList: mission.triggerList = []
        mission.triggerList.append(CreateTrigger(0, 'objective-primary', 'destroy-class', "", 'primary', display_text = 'Destroy the enemy fighters'))
        mission.triggerList.append(CreateTrigger(1, 'objective-secondary', 'survive-class', "", 'ally', display_text = 'Keep your squad alive'))
        mission.triggerList.append(CreateTrigger(2, 'objective-primary', 'survive-attached', "", '', display_text = 'You must survive!'))
        mission.triggerList[len(mission.triggerList) - 1].parent = mission.spawnList[0]
        
        return mission
    
    
class CampaignMenu(Frame):
    '''
    This will handle the major menu interactions that the player has with the campaign system 
    '''
    campaign = None
    manager = None
    
    background = None
    
    mission_start = None
    ship_list = None
    
    save_btn = None
    load_btn = None
    back_btn = None
    new_btn = None
    
    fleet_image = None
    arrow_image = None
    
    battle_btns = None
    cur_battles = None
    
    def __init__(self, parent, **kwargs):
        super(CampaignMenu, self).__init__(parent, **kwargs)
        
        self.manager = kwargs.get('manager', None)
        self.campaign = kwargs.get('campaign', None)
        self.mission_start = kwargs.get('mission_start', None)
        self.ship_list = kwargs.get('ship_list', None)
        if self.manager and not self.campaign:
            self.campaign = self.manager.create_new_random()
            self.manager.currentCampaign = self.campaign
        
        self.fleet_image, r = Utils.load_image("fleet_logo.png", -1)
        
        self.arrow_image, r = Utils.load_image("battle_arrow.png", -1)
        
        self.battle_btns = []
        
        self.init()
        
    def init(self):
        '''
        initializes stuff - should be called whenever the campaign changes
        '''
        self.children = []
        
        BasicTextButton(self, text = "Do Turn", callback = self.campaign.do_turn)
        
        for p in self.campaign.planets:
            PlanetButton(self, planet = p)#, callback = self.planet_click, callback_kwargs = {'value': p})
        
        for f in self.campaign.fleets:
            FleetImageLabel(self, f, image = self.fleet_image)
            
        self.cur_battles = self.campaign.battles[:]
        self.refresh_battle_btns()
        
        offset, block_size = self.get_offset_and_block_size()
        
        left = offset[0] + offset[2]
        top = offset[1]
        
        # back button
        img = Utils.load_image("back.png", -1)[0]
        self.back_btn = BasicImageButton(self, selected_image = img, unselected_image = img, callback = self.back_btn_click)
        self.back_btn.rect.topleft = (left - self.back_btn.rect.width, top)
        top += self.back_btn.rect.height + 2
        
        # new button
        img = Utils.load_image("new.png", -1)[0]
        self.new_btn = BasicImageButton(self, selected_image = img, unselected_image = img, callback = self.new_btn_click)
        self.new_btn.rect.topleft = (left - self.new_btn.rect.width, top)
        top += self.new_btn.rect.height + 2
        
        # load button
        img = Utils.load_image("load.png", -1)[0]
        self.load_btn = BasicImageButton(self, selected_image = img, unselected_image = img, callback = self.load_btn_click)
        self.load_btn.rect.topleft = (left - self.load_btn.rect.width, top)
        top += self.load_btn.rect.height + 2
        
        # save button
        img = Utils.load_image("save.png", -1)[0]
        self.save_btn = BasicImageButton(self, selected_image = img, unselected_image = img, callback = self.save_btn_click)
        self.save_btn.rect.topleft = (left - self.save_btn.rect.width, top)
        top += self.save_btn.rect.height + 2
        
    
    def refresh_battle_btns(self):
        for b in self.cur_battles:
            vec = Vec2(0,0)
            vec.setXY(b.end[0] - b.start[0], b.end[1] - b.start[1])
            img = pygame.transform.rotate(self.arrow_image.copy(), vec.theta)
            self.battle_btns.append(BattleButton(self, battle = b, image = img, callback = self.battle_click, callback_kwargs = {'value': b}))
            
        
    def get_offset_and_block_size(self):
        width = pygame.display.get_surface().get_width() 
        if width > consts.DEFAULT_WINDOW_WIDTH:
            width = consts.DEFAULT_WINDOW_WIDTH
        
        height = pygame.display.get_surface().get_height()
        if height > consts.DEFAULT_WINDOW_HEIGHT:
            height = consts.DEFAULT_WINDOW_HEIGHT
        
        offset = ((pygame.display.get_surface().get_width() - width) * 0.5, (pygame.display.get_surface().get_height() - height) * 0.5, width, height)
        
        if self.campaign.boardSize[0] > 0:
            width /= self.campaign.boardSize[0]
        else:
            width /= DEFAULT_BOARD_WIDTH
            
        if self.campaign.boardSize[1] > 0:
            height /= self.campaign.boardSize[1]
        else:
            height /= DEFAULT_BOARD_HEIGHT
            
        block_size = (width, height)
        
        
        return offset, block_size
        
        
    def draw(self):
        offset, block_size = self.get_offset_and_block_size()
        
        self.background = pygame.surface.Surface((offset[2], offset[3]))
        self.background.fill((0,0,0), self.background.get_rect())
        pygame.gfxdraw.rectangle(self.background, self.background.get_rect(), consts.COLOR_ORANGE)
        
        if not set(self.cur_battles) == set(self.campaign.battles):
            # need to refresh the battle buttons
            for b in self.battle_btns:
                 self.children.remove(b)
            self.battle_btns = []
            
            self.cur_battles = self.campaign.battles[:]
            self.refresh_battle_btns()
        
        pygame.display.get_surface().blit(self.background, offset)
        for c in self.children:
            if isinstance(c, PlanetButton):
                c.rect.topleft = offset[0] + c.planet.boardPosition[0] * block_size[0], offset[1] + c.planet.boardPosition[1] * block_size[1]
                c.draw()
            elif isinstance(c, FleetImageLabel):
                c.rect.topleft = offset[0] + c.fleet.board_position[0] * block_size[0], offset[1] + c.fleet.board_position[1] * block_size[1]
                c.draw()
            elif isinstance(c, BattleButton):
                c.rect.topleft = offset[0] + (c.battle.start[0] + c.battle.end[0]) * 0.5 * block_size[0], offset[1] + (c.battle.start[1] + c.battle.end[1]) * 0.5 * block_size[1]
                c.draw()
            else:
                c.draw()
            
    def update(self, event):
        super(CampaignMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()
    
    def back_btn_click(self, **kwargs):
        self.parent.main_menu_click()
    
    def save_btn_click(self, **kwargs):
        pass
    
    def load_btn_click(self, **kwargs):
        pass
    
    def new_btn_click(self, **kwargs):
        
        self.set_active(False)
        self.manager.create_new_random()
        self.manager.currentCampaign = self.manager.campaignList[len(self.manager.campaignList) - 1]
        self.manager.show_display(self.parent)
    
    def test(self, who):
        print "test!"
        
    def planet_click(self, **kwargs):
        '''
        for right now, lets randomly generate a mission based on the planet's strength value - assuming that the player is on the "red" team
        TODO change this to actually interact with the planets in some way?
        '''
        
        planet = kwargs.get('value', None)
        if not planet: return
        
        # get the mission
        mission = planet.get_mission(self.ship_list)
        
        # start the mission
        self.mission_start(mission)
        
    def battle_click(self, **kwargs):
        pass
        
class PlanetButton(BasicImageButton):
    planet = None
    font = None
    
    def __init__(self, parent, **kwargs):
        self.planet = kwargs.get('planet')
        
        super(PlanetButton, self).__init__(parent, image = self.planet.sprite.image, **kwargs)
        
        self.font = kwargs.get('font', pygame.font.Font(None, 20))
        
        self.update_image()
        
    def update(self, event):
        super(PlanetButton, self).update(event)
        
    def draw(self):
        super(PlanetButton, self).draw()
        
    def update_image(self):
        text = "(%i) %s" % (self.planet.strength, self.planet.name)
        fsize = self.font.size(text)
        w = self.planet.sprite.image.get_width()
        if fsize[0] > w: w = fsize[0]
        img = pygame.surface.Surface((w, self.planet.sprite.image.get_height() + fsize[1]))
        img.convert()
        img.set_colorkey(img.get_at((0,0)))
        if w > self.planet.sprite.image.get_width():
            img.blit(self.planet.sprite.image, ((w - self.planet.sprite.image.get_width()) * 0.5, 0))
        else:
            img.blit(self.planet.sprite.image, (0,0))
        
        color = (255, 255, 255)
        if self.planet.faction and 'color' in self.planet.faction:
            color = self.planet.faction['color']
        img.blit(self.font.render(text, 1, color),
                                          ((w - fsize[0]) * 0.5, self.planet.sprite.image.get_height()))
        
        selected = False
        if self.image is self.selected_image:
            selected = True
            
        self.unselected_image = img
        self.selected_image = self.generate_selected_image(img)
        if selected:
            self.image = self.selected_image
        else:
            self.image = self.unselected_image
        
    def on_mouse_over(self):
        pass
    
    def on_mouse_off(self):
        pass
        
class FleetImageLabel(ImageLabel):
    fleet = None
    
    def __init__(self, parent, fleet, **kwargs):
        super(FleetImageLabel, self).__init__(parent, **kwargs)
        self.fleet = fleet

class BattleButton(BasicImageButton):
    battle = None
    
    def __init__(self, parent, battle, **kwargs):
        super(BattleButton, self).__init__(parent, **kwargs)
        
        self.battle = battle
