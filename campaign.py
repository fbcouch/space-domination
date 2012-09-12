'''
Created on Sep 12, 2012

@author: Jami
'''
import Utils
import math
import pygame
import random

DEFAULT_PLANETS = 10
DEFAULT_BOARD_WIDTH = 10
DEFAULT_BOARD_HEIGHT = 10


class CampaignManager(object):
    '''
    CampaignManager will basically handle setting up the current campaign for us and creating the relevant menus, etc
    '''
    campaignList = None
    currentCampaign = None
    
    context = None
    
    
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
                    
            planetList.append(planet)
            print "%s (%i, %i)" % (planet.name, planet.boardPosition[0], planet.boardPosition[1])
        
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
        
        
class Campaign(object):
    '''
    Contains the status of a campaign...this theoretically should be saved/loaded from files
    '''
    pass

class Planet(object):
    '''
    Within the context of a campaign, there will be planets with some attributes such as defense level, etc
    '''
    file = None
    sprite = None
    boardPosition = None
    name = None
    
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
        
        
        
        
        