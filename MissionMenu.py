'''
Created on Aug 18, 2012

@author: Jami
'''
from gui.basicmenu import BasicImageButton, BasicTextButton, \
    TogglableImageButton, PagedMenu
from gui.gui import Frame, Element
import Utils
import pygame
    
class MissionMenu(PagedMenu):
    '''Frame implementation to display the mission selection menu'''
    
    mission_start = None
    missions = None
    
    name_label = None
    desc_label = None
    
    selected_mission = None
    title_color = None
    desc_color = None
    desc_max_width = 1024
    
    def __init__(self, parent, mission_start, **kwargs):
        
        if not 'back_btn_text' in kwargs: kwargs['back_btn_text'] =  '< Back to Main Menu'
        if not 'back_btn_callback' in kwargs: kwargs['back_btn_callback'] = parent.main_menu_click
        if not 'item_callback' in kwargs: kwargs['item_callback'] = self.mission_click
        self.missions = kwargs.get('missions', None)
        if self.missions:
            items = []
            for mission in self.missions:
                items.append((mission[1], mission))
            kwargs['items'] = items
        
        super(MissionMenu, self).__init__(parent, **kwargs)
        
        self.mission_start = mission_start
        self.title_color = kwargs.get('title_color', (255, 255, 100))
        self.desc_color = kwargs.get('desc_color', (200, 200, 200))
        self.desc_max_width = int(kwargs.get('desc_width', 1024))
        
    def draw(self):
        '''draws the mission selection screen'''
        draw_rect = super(MissionMenu, self).draw()
        screen = pygame.display.get_surface()
        
        # draw the mission info
        if self.selected_mission:
            y = draw_rect.top + draw_rect.height + self.v_pad * 3
            size = self.font.size(self.selected_mission[2])
            x = (screen.get_width() - size[0]) * 0.5
            screen.blit(self.font.render(self.selected_mission[2], 1, self.title_color), (x, y))
            if x < draw_rect.left: draw_rect.left = x
            
            # break the description up into lines if necessary
            y += size[1] + self.v_pad
            lines = Utils.parse(self.selected_mission[3], self.desc_max_width, self.font)
            size = [0,0]
            for line in lines:
                sz = self.font.size(line)
                size[1] += sz[1]
                if sz[0] > size[0]: size[0] = sz[0]
            
            x = (screen.get_width() - size[0]) * 0.5
            for line in lines:
                screen.blit(self.font.render(line, 1, self.desc_color), (x, y))
                y += self.font.size(line)[1]
                if x < draw_rect.left: draw_rect.left = x
            draw_rect.height = y - draw_rect.top
        return draw_rect
            
    def update(self, event):
        if super(MissionMenu, self).update(event):
            return True
        
        
        return False
    
    
    
    
    def mouse_over_callback(self, child):
        if self.selected_item and self.selected_item is not child:
            self.selected_item.on_mouse_off()
        self.selected_mission = child.callback_kwargs.get('value', None)
        self.selected_item = child
        
    def mouse_off_callback(self, child):
        pass#if self.selected_mission is child.callback_kwargs.get('value', None): self.selected_mission = None
    
    def mission_click(self, **kwargs):
        mission = kwargs.get('value', None)
        self.parent.close()
        if mission and self.mission_start and mission in self.missions:
            self.mission_start(mission)
        