'''
Created on Aug 20, 2012

@author: Jami
'''
from consts import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from gui.gui import Frame, Element
import consts
import pygame

class ProfileMenu(Frame):
    '''handles the display and user manipulations for the profile list and currently selected profile'''
    
    current_profile = None
    profile_list = None
    set_profile_fxn = None
    
    profile_view = None
    profile_edit = None
    profile_add = None
    profile_delete = None
    
    
    def __init__(self, parent, profile, profiles, set_profile, **kwargs):
        '''Constructor'''
        super(ProfileMenu, self).__init__(parent, **kwargs)
        
        self.current_profile = profile
        self.profile_list = profiles
        self.set_profile_fxn = set_profile
        
        self.set_profile_view(self.current_profile)
    
    def update(self, event):
        '''updates the menu based on the event'''
        returnVal = super(ProfileMenu, self).update(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()
        
        return returnVal
        
    def draw(self):
        super(ProfileMenu, self).draw()
        
    def set_profile_view(self, profile = None):
        if profile and profile is not self.current_profile and profile in self.profile_list:
            self.current_profile = profile
            self.set_profile_fxn(self.current_profile)
        
        if not self.profile_view:
            # create the menu anew:
            self.profile_view = ProfileView(self, self.current_profile)
        else:
            # update the current view menu
            self.profile_view.set_profile(self.current_profile)
            
        if not self.profile_view in self.children:
            self.add_child(self.profile_view)
        
        self.profile_view.set_active(True)
            
class ProfileView(Frame):
    '''handles the display of the current profile'''
    
    profile = None
    v_pad = 0
    
    
    def __init__(self, parent, profile, **kwargs):
        '''Constructor'''
        super(ProfileView, self).__init__(parent, **kwargs)
        self.profile = profile
        self.v_pad = kwargs.get('v_pad', 5)
        self.init()
        
    def init(self):
        '''initializes the view'''
        
        x = 0
        y = 0
        self.children = []
        lb = Label(self, "Callsign: %s" % self.profile['name'])
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        if not 'shots-fired' in self.profile:
            self.profile['shots-fired'] = 0
        if not 'shots-hit' in self.profile:
            self.profile['shots-hit'] = 0
        if not 'kills' in self.profile:
            self.profile['kills'] = 0
        if not 'deaths' in self.profile:
            self.profile['deaths'] = 0
        if not 'damage-dealt' in self.profile:
            self.profile['damage-dealt'] = 0
        if not 'damage-taken' in self.profile:
            self.profile['damage-taken'] = 0
        
        if int(self.profile['deaths']) > 0:
            ratio = float(self.profile['kills']) / float(self.profile['deaths'])
        else:
            ratio = float(self.profile['kills'])
        ratio_dec = int((ratio - int(ratio)) * 10)
        lb = Label(self, "Kills: %i" % int(self.profile['kills']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "Deaths: %i" % int(self.profile['deaths']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "K/D Ratio: %i.%i" % (int(ratio), int(ratio_dec)))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        if float(self.profile['shots-fired']) > 0:
            accuracy = float(self.profile['shots-hit']) / float(self.profile['shots-fired']) * 100
        else:
            accuracy = 0.0
        accuracy_dec = int((accuracy - int(accuracy)) * 10)
        
        lb = Label(self, "Shots Hit: %i" % int(self.profile['shots-hit']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "Shots Fired: %i" % int(self.profile['shots-fired']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "Accuracy: %i.%i" % (int(accuracy), accuracy_dec))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "Damage Dealt: %i" % int(self.profile['damage-dealt']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        lb = Label(self, "Damage Taken: %i" % int(self.profile['damage-taken']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        
        
        
    def set_profile(self, profile):
        self.profile = profile
        self.init()
        
    def get_profile(self):
        return self.profile
    
    def draw(self):
        screen = pygame.display.get_surface()
        
        draw_rect = pygame.rect.Rect(0, 0, 0, 0)
        for child in self.children:
            if child.is_active():
                if child.rect.left + child.rect.width > draw_rect.width:
                    draw_rect.width = child.rect.left + child.rect.width
                if child.rect.top + child.rect.height > draw_rect.height:
                    draw_rect.height = child.rect.top + child.rect.height
                    
        offset_x = (screen.get_rect().width - draw_rect.width) * 0.5
        offset_y = (screen.get_rect().height - draw_rect.height) * 0.5
        for child in self.children:
            if child.is_active():
                save_rect = child.rect.copy()
                child.rect.topleft = (child.rect.left + offset_x, child.rect.top + offset_y)
                child.draw()
                child.rect = save_rect
        
        
        
    
class Label(Element):
    '''displays static text'''
    
    text = None
    font = None
    color = None
    
    def __init__(self, parent, text, **kwargs):
        super(Label, self).__init__(parent, **kwargs)
        self.text = text
        self.font = kwargs.get('font', pygame.font.Font(None, 24))
        self.color = kwargs.get('color', (255,255,255))
        self.rect = None
        self.init()
        
    def init(self):
        '''initializes'''
        self.image = self.font.render(self.text, 1, self.color)
        if self.rect:
            rect = self.image.get_rect()
            self.rect.width = rect.width
            self.rect.height = rect.height
        else:
            self.rect = self.image.get_rect()
        
    def set_text(self, text):
        self.text = text
        self.init()
    
    def get_text(self):
        return self.text
        