'''
Created on Aug 14, 2012

@author: Jami
'''
import consts
import pygame

class Profile(dict):
    '''
    Contains all the information necessary for a profile
    '''
    shiplist = None
    
    def __init__(self):
        self.shiplist = {}
    
def create_profile_from_attrs(attrs, default_id = -1):
    keys = attrs.keys()
    profile = Profile()
    for key in keys:
        profile[key] = attrs.get(key)
    if int(profile['id']) == default_id:
        profile['active'] = True
    return profile
    
    
def create_fresh_profile(**kwargs):
    list = kwargs.get('profiles', None)
    id = kwargs.get('id', -1)
    if id == -1 and list:
        for p in list:
            if 'id' in p and int(p['id']) > id:
                id = int(p['id'])
        id += 1
    
    profile = Profile()
    profile['id'] = id
    profile['name'] = 'newbie'
    profile['ship'] = 0
    disp = pygame.display.get_surface()
    if disp:
        profile['width'] = pygame.display.get_surface().get_width()
        profile['height'] = pygame.display.get_surface().get_height()
    else:
        profile['width'] = consts.DEFAULT_WINDOW_WIDTH
        profile['height'] = consts.DEFAULT_WINDOW_HEIGHT
    profile['fullscreen'] = False
    
    return profile