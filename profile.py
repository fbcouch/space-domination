'''
Created on Aug 14, 2012

@author: Jami
'''

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
    