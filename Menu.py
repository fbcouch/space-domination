'''
Created on Aug 17, 2012

@author: Jami
'''
from MissionMenu import MissionMenu
from ProfileMenu import ProfileMenu
from gui.basicmenu import BasicMenu, BasicTextButton, BasicImageButton, \
    BasicTextInput
from gui.gui import GUI, Frame, Element
import Utils
import pygame

class SpaceDominationGUI(GUI):
    '''GUI implentation for Space Domination'''
    
    def __init__(self, parent, **kwargs):
        super(SpaceDominationGUI, self).__init__(parent, **kwargs)
        
        # set up the main menu
        self.main_menu = BasicMenu(self, h_pad = 5, v_pad = 5)
        self.add_child(self.main_menu)
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Select Mission', select_fxn = self.main_menu.mouse_over_callback, callback = self.mission_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Profiles', select_fxn = self.main_menu.mouse_over_callback, callback = self.profile_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Options', select_fxn = self.main_menu.mouse_over_callback, callback = self.options_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Exit', select_fxn = self.main_menu.mouse_over_callback, callback = self.exit_click))
        
        # TODO add/set up the mission menu
        self.mission_menu = MissionMenu(self, self.parent.startMission, missions = self.parent.missionList)
        self.add_child(self.mission_menu)
        
        # add/set up the profile menu
        self.profile_menu = ProfileMenu(self, self.parent.currentProfile, self.parent.profiles, self.parent.setActiveProfile)
        self.add_child(self.profile_menu)
        
        # add/set up the options menu
        self.options_menu = BasicMenu(self, h_pad = 5, v_pad = 5, on_close = self.main_menu_click)
        self.add_child(self.options_menu)
        BasicTextInput(self.options_menu, label = 'Screen Width', value = self.parent.currentProfile['width'], numbers_only = True, select_fxn = self.options_menu.mouse_over_callback)
        BasicTextInput(self.options_menu, label = 'Screen Height', value = self.parent.currentProfile['height'], numbers_only = True, select_fxn = self.options_menu.mouse_over_callback)
        BasicTextButton(self.options_menu, text = 'Apply Changes', select_fxn = self.options_menu.mouse_over_callback, callback = self.apply_options)
        BasicTextButton(self.options_menu, text = 'Back to Main Menu', select_fxn = self.options_menu.mouse_over_callback, callback = self.main_menu_click)
        
        # add/set up the pause menu
        self.pause_menu = PauseMenu(self, self.parent.unpause_game, h_pad = 5, v_pad = 5)
        self.add_child(self.pause_menu)
        BasicTextButton(self.pause_menu, text = 'Resume', select_fxn = self.pause_menu.mouse_over_callback, callback = self.parent.unpause_game)
        self.pause_menu.add_child(BasicTextButton(self.pause_menu, text = 'Options', select_fxn = self.pause_menu.mouse_over_callback, callback = self.options_menu_click))
        self.pause_menu.add_child(BasicTextButton(self.pause_menu, text = 'Exit', select_fxn = self.pause_menu.mouse_over_callback, callback = self.exit_click))
        
    def apply_options(self):
        '''apply the height/width options'''
        self.parent.currentProfile['width'] = int(self.options_menu.children[0].value)
        self.parent.currentProfile['height'] = int(self.options_menu.children[1].value)
        self.parent.createDisplay()
        self.parent.saveProfiles()
        self.options_menu.children[0].value = self.parent.currentProfile['width']
        self.options_menu.children[1].value = self.parent.currentProfile['height']
        self.options_menu.children[0].set_unselected_image()
        self.options_menu.children[1].set_unselected_image()

class PauseMenu(BasicMenu):
    
    unpause_fxn = None
    
    def __init__(self, parent, unpause_fxn, **kwargs):
        super(PauseMenu, self).__init__(parent, **kwargs)
        
        self.unpause_fxn = unpause_fxn
    
    def update(self, event):
        super(PauseMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.unpause_fxn: self.unpause_fxn()
        

    
    
    