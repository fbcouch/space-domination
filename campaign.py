'''
Created on Sep 12, 2012

@author: Jami
'''
from gui.basicmenu import BasicImageButton
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
        factions = [{'name': "Red team", 'color': consts.COLOR_RED}, {'name': "Blue team", 'color': consts.COLOR_BLUE}]
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
            
            planet.faction = factions[random.randint(0, len(factions) - 1)]    
            planet.strength = random.randint(1, 3)
            planetList.append(planet)
        
        cp = Campaign()
        cp.planets = planetList
        cp.factions = factions
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
        self.display = CampaignMenu(parent, campaign = self.currentCampaign, manager = self)
        parent.add_child(self.display)
        self.display.set_active(True)
        
class Campaign(object):
    '''
    Contains the status of a campaign...this theoretically should be saved/loaded from files
    '''
    planets = None
    boardSize = None
    factions = None
    
    def __init__(self):
        self.planets = []
        self.boardSize = (0,0)
        self.factions = []
        
    

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
        
class CampaignMenu(Frame):
    '''
    This will handle the major menu interactions that the player has with the campaign system 
    '''
    campaign = None
    manager = None
    
    background = None
    
    def __init__(self, parent, **kwargs):
        super(CampaignMenu, self).__init__(parent, **kwargs)
        
        self.manager = kwargs.get('manager', None)
        self.campaign = kwargs.get('campaign', None)
        if self.manager and not self.campaign:
            self.campaign = self.manager.create_new_random()
            self.manager.currentCampaign = self.campaign
        
        self.init()
        
    def init(self):
        '''
        initializes stuff - should be called whenever the campaign changes
        '''
        for p in self.campaign.planets:
            PlanetButton(self, planet = p)
        
    def draw(self):
        
        width = pygame.display.get_surface().get_width() 
        if width > consts.DEFAULT_WINDOW_WIDTH:
            width = consts.DEFAULT_WINDOW_WIDTH
        
        height = pygame.display.get_surface().get_height()
        if height > consts.DEFAULT_WINDOW_HEIGHT:
            height = consts.DEFAULT_WINDOW_HEIGHT
        
        offset = ((pygame.display.get_surface().get_width() - width) * 0.5, (pygame.display.get_surface().get_height() - height) * 0.5) 
        self.background = pygame.surface.Surface((width, height))
        self.background.fill((0,0,0), self.background.get_rect())
        pygame.gfxdraw.rectangle(self.background, self.background.get_rect(), consts.COLOR_ORANGE)
        
        if self.campaign.boardSize[0] > 0:
            width /= self.campaign.boardSize[0]
        else:
            width /= DEFAULT_BOARD_WIDTH
            
        if self.campaign.boardSize[1] > 0:
            height /= self.campaign.boardSize[1]
        else:
            height /= DEFAULT_BOARD_HEIGHT
            
        block_size = (width, height)
        
        pygame.display.get_surface().blit(self.background, offset)
        for c in self.children:
            if isinstance(c, PlanetButton):
                c.rect.topleft = offset[0] + c.planet.boardPosition[0] * block_size[0], offset[1] + c.planet.boardPosition[1] * block_size[1]
                c.draw()
            
    def update(self, event):
        super(CampaignMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()
        
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
        
        
        
    
    