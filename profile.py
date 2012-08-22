'''
Created on Aug 14, 2012

@author: Jami
'''
import pygame

class Profile(dict):
    '''
    Contains all the information necessary for a profile
    '''
    
    
def create_profile_from_attrs(attrs, default_id = -1):
    keys = attrs.keys()
    profile = Profile()
    for key in keys:
        profile[key] = attrs.get(key)
    if int(profile['id']) == default_id:
        profile['active'] = True
    return profile
    
    
def create_fresh_profile():
    profile = Profile()
    profile['name'] = 'newbie'
    profile['ship'] = 0
    profile['width'] = pygame.display.get_surface().get_width()
    profile['height'] = pygame.display.get_surface().get_height()
    
    return profile