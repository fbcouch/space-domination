'''
Created on Aug 17, 2012

@author: Jami
'''
from MissionMenu import MissionMenu
from ProfileMenu import ProfileMenu
from gui.basicmenu import BasicMenu, BasicTextButton, BasicImageButton, \
    BasicTextInput, Label
from gui.gui import GUI, Frame, Element
import Utils
import consts
import pygame

class SpaceDominationGUI(GUI):
    '''GUI implentation for Space Domination'''
    mission_results = None
    
    def __init__(self, parent, **kwargs):
        super(SpaceDominationGUI, self).__init__(parent, **kwargs)
        
        # set up the main menu
        self.main_menu = BasicMenu(self, h_pad = 5, v_pad = 5)
        self.add_child(self.main_menu)
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Select Mission', select_fxn = self.main_menu.mouse_over_callback, callback = self.mission_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Campaigns', select_fxn = self.main_menu.mouse_over_callback, callback = self.campaign_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Profiles', select_fxn = self.main_menu.mouse_over_callback, callback = self.profile_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Options', select_fxn = self.main_menu.mouse_over_callback, callback = self.options_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Exit', select_fxn = self.main_menu.mouse_over_callback, callback = self.exit_click))
        
        # TODO add/set up the mission menu
        self.mission_menu = MissionMenu(self, self.parent.startMission, missions = self.parent.missionList)
        self.add_child(self.mission_menu)
        
        # add/set up the profile menu
        #self.profile_menu = ProfileMenu(self, self.parent.currentProfile, self.parent.profiles, self.parent.setActiveProfile, shiplist = self.parent.shipList)
        #self.add_child(self.profile_menu)
        
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
        BasicTextButton(self.pause_menu, text = 'Quit Mission', select_fxn = self.pause_menu.mouse_over_callback, callback = self.parent.quit_mission)
        BasicTextButton(self.pause_menu, text = 'Options', select_fxn = self.pause_menu.mouse_over_callback, callback = self.options_menu_click)
        BasicTextButton(self.pause_menu, text = 'Exit', select_fxn = self.pause_menu.mouse_over_callback, callback = self.exit_click)
        
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
        
    def profile_menu_click(self):
        if self.profile_menu and self.profile_menu in self.children:
            self.children.remove(self.profile_menu)
        
        self.profile_menu = ProfileMenu(self, self.parent.currentProfile, self.parent.profiles, self.parent.setActiveProfile, self.parent.saveProfiles, shiplist = self.parent.shipList)
        self.add_child(self.profile_menu)
        
        super(SpaceDominationGUI, self).profile_menu_click()
        
    def campaign_menu_click(self):
        if self.parent.campaignMgr:
            for child in self.children:
                child.set_active(False)
            self.parent.campaignMgr.show_display(self)
            
    def mission_results_show(self, result, mission):
        if not self.mission_results:
            self.mission_results = MissionResultsMenu(self, self.main_menu_click, self.campaign_menu_click, mission, self.parent.largefont)
            self.add_child(self.mission_results)
        self.mission_results.init(result, mission)
        self.generic_click(target_id = self.children.index(self.mission_results))
        
class PauseMenu(BasicMenu):
    
    unpause_fxn = None
    
    def __init__(self, parent, unpause_fxn, **kwargs):
        super(PauseMenu, self).__init__(parent, **kwargs)
        
        self.unpause_fxn = unpause_fxn
    
    def update(self, event):
        super(PauseMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.unpause_fxn: self.unpause_fxn()
        
class MissionResultsMenu(Frame):
    
    default_back_fxn = None
    campaign_back_fxn = None
    mission = None
    font = None
    
    resultLabel = None
    backBtn = None
    
    def __init__(self, parent, default_back_fxn, campaign_back_fxn, mission, font, **kwargs):
        super(MissionResultsMenu, self).__init__(parent, **kwargs)
        
        self.default_back_fxn = default_back_fxn
        self.campaign_back_fxn = campaign_back_fxn
        self.mission = mission
        self.font = font
    
    def init(self, result, mission = None):
        if mission:
            self.mission = mission
        
        if result:
            text = "MISSION COMPLETE"
            color = consts.COLOR_GREEN
        else:
            text = "MISSION FAILED"
            color = consts.COLOR_RED
            
        if not self.resultLabel:
            self.resultLabel = Label(self, text, font = self.font, color = color)
        else:
            self.resultLabel.set_text(text)
            self.resultLabel.color = color
            
        self.resultLabel.rect.center = (pygame.display.get_surface().get_width() * 0.5, 150)
            
    def update(self, event):
        super(MissionResultsMenu, self).update(event)
        
        if self.resultLabel:
            self.resultLabel.rect.center = (pygame.display.get_surface().get_width() * 0.5, 150)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.mission and self.mission.isCampaignMission:
                if self.campaign_back_fxn: self.campaign_back_fxn()
                return True
            else:
                if self.default_back_fxn: self.default_back_fxn()
                return True
                