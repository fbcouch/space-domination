'''
Created on Aug 17, 2012

@author: Jami
'''
from gui.basicmenu import BasicMenu, BasicTextButton, BasicImageButton
from gui.gui import GUI, Frame
import Utils
import pygame

class SpaceDominationGUI(GUI):
    '''GUI implentation for Space Domination'''
    
    def __init__(self, parent, **kwargs):
        super(SpaceDominationGUI, self).__init__(parent, **kwargs)
        
        # set up the main menu
        self.main_menu = BasicMenu(self, h_pad = 10, v_pad = 10)
        self.add_child(self.main_menu)
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Select Mission', select_fxn = self.main_menu.mouse_over_callback, callback = self.mission_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Profiles', select_fxn = self.main_menu.mouse_over_callback, callback = self.profile_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Options', select_fxn = self.main_menu.mouse_over_callback, callback = self.options_menu_click))
        self.main_menu.add_child(BasicTextButton(self.main_menu, text = 'Exit', select_fxn = self.main_menu.mouse_over_callback, callback = self.exit_click))
        
        # TODO add/set up the mission menu
        self.mission_menu = MissionMenu(self, self.parent.startMission, missions = self.parent.missionList)
        self.add_child(self.mission_menu)
        
        # TODO add/set up the profile menu
        
        # TODO add/set up the options menu
        
        # add/set up the pause menu
        self.pause_menu = PauseMenu(self, self.parent.unpause_game, h_pad = 10, v_pad = 10)
        self.add_child(self.pause_menu)
        BasicTextButton(self.pause_menu, text = 'Resume', select_fxn = self.pause_menu.mouse_over_callback, callback = self.parent.unpause_game)
        self.pause_menu.add_child(BasicTextButton(self.pause_menu, text = 'Options', select_fxn = self.pause_menu.mouse_over_callback, callback = self.options_menu_click))
        self.pause_menu.add_child(BasicTextButton(self.pause_menu, text = 'Exit', select_fxn = self.pause_menu.mouse_over_callback, callback = self.exit_click))

class PauseMenu(BasicMenu):
    
    unpause_fxn = None
    
    def __init__(self, parent, unpause_fxn, **kwargs):
        super(PauseMenu, self).__init__(parent, **kwargs)
        
        self.unpause_fxn = unpause_fxn
    
    def update(self, event):
        super(PauseMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.unpause_fxn: self.unpause_fxn()
        
class MissionMenu(Frame):
    '''Frame implementation to display the mission selection menu'''
    
    mission_start = None
    
    missions = None
    page = 1
    num_per_page = 4
    
    next_btn = None
    prev_btn = None
    page_indicator = None
    
    name_label = None
    desc_label = None
    
    h_pad = 0
    v_pad = 0
    
    selected_mission = None
    title_color = None
    desc_color = None
    
    font = None
    
    def __init__(self, parent, mission_start, **kwargs):
        super(MissionMenu, self).__init__(parent, **kwargs)
        
        self.mission_start = mission_start
        self.num_per_page = int(kwargs.get('per_page', 4))
        self.h_pad = int(kwargs.get('h_pad', 50))
        self.v_pad = int(kwargs.get('v_pad', 10))
        self.missions = kwargs.get('missions', [])
        self.build_from_mission_list()
        self.title_color = kwargs.get('title_color', (255, 255, 255))
        self.desc_color = kwargs.get('desc_color', (255, 255, 255))
        self.font = kwargs.get('font', pygame.font.Font(None, 24))
        
        
        
    def build_from_mission_list(self, missions = None):
        '''build the mission list using the list of mission...'''
        if missions:
            self.missions = missions
        
        n = 0
        for mission in self.missions:
            # add a button to the child list for each mission
            n += 1
            
            self.add_child(BasicImageButton(self, image = mission[1], select_fxn = self.mouse_over_callback, callback = self.mission_click, callback_kwargs = {'mission':mission}))
    
    def update(self, event):
        super(MissionMenu, self).update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()

    def draw(self):
        '''draws the mission selection screen'''
        screen = pygame.display.get_surface()
        num_pages = len(self.missions) / float(self.num_per_page)
        if num_pages > int(num_pages): num_pages = int(num_pages) + 1
        
        if self.page < 1: self.page = 1
        
        start_i = (self.page - 1) * self.num_per_page
        end_i = self.page * self.num_per_page
        if end_i > len(self.missions): end_i = len(self.missions)
        
        # first, calculate the draw rect
        draw_rect = pygame.rect.Rect(0,0,0,0)
        for i in range(start_i, end_i):
            child = self.children[i]
            if child.rect.height > draw_rect.height:
                draw_rect.height = child.rect.height
            if i > 0:
                draw_rect.width += self.h_pad
            draw_rect.width += child.rect.width
        
        # now, center the rect
        draw_rect.center = screen.get_rect().center
        
        # now, draw these buttons
        x = draw_rect.left
        for i in range(start_i, end_i):
            child = self.children[i]
            y = draw_rect.top + (draw_rect.height - child.rect.height) * 0.5
            child.rect.topleft = (x, y)
            child.draw()
            x += child.rect.width + self.h_pad
        
        # TODO draw the page display and prev/next buttons
        
        # draw the mission info
        if self.selected_mission:
            y = draw_rect.top + draw_rect.height + self.v_pad * 3
            size = self.font.size(self.selected_mission[2])
            x = (screen.get_width() - size[0]) * 0.5
            screen.blit(self.font.render(self.selected_mission[2], 1, self.title_color), (x, y))
            
            y += size[1] + self.v_pad
            size = self.font.size(self.selected_mission[3])
            x = (screen.get_width() - size[0]) * 0.5
            screen.blit(self.font.render(self.selected_mission[3], 1, self.desc_color), (x, y))
            
        
    def mouse_over_callback(self, child):
        self.selected_mission = child.callback_kwargs.get('mission', None)
    
    def mission_click(self, **kwargs):
        mission = kwargs.get('mission', None)
        self.parent.close()
        if mission and self.mission_start and mission in self.missions:
            self.mission_start(mission)
        
        