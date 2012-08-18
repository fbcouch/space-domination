'''
Created on Aug 18, 2012

@author: Jami
'''
from gui.basicmenu import BasicImageButton, BasicTextButton, \
    TogglableImageButton
from gui.gui import Frame, Element
import Utils
import pygame

class MissionMenu(Frame):
    '''Frame implementation to display the mission selection menu'''
    
    mission_start = None
    
    missions = None
    page = 1
    num_per_page = 4
    
    next_btn = None
    prev_btn = None
    page_indicator = None
    back_btn = None
    
    name_label = None
    desc_label = None
    
    h_pad = 0
    v_pad = 0
    
    selected_mission = None
    title_color = None
    desc_color = None
    desc_max_width = 1024
    
    font = None
    
    def __init__(self, parent, mission_start, **kwargs):
        super(MissionMenu, self).__init__(parent, **kwargs)
        
        self.mission_start = mission_start
        self.num_per_page = int(kwargs.get('per_page', 4))
        self.h_pad = int(kwargs.get('h_pad', 50))
        self.v_pad = int(kwargs.get('v_pad', 10))
        self.missions = kwargs.get('missions', [])
        self.build_from_mission_list()
        self.title_color = kwargs.get('title_color', (255, 255, 100))
        self.desc_color = kwargs.get('desc_color', (200, 200, 200))
        self.desc_max_width = int(kwargs.get('desc_width', 1024))
        self.font = kwargs.get('font', pygame.font.Font(None, 24))
        
        arrows = Utils.load_sprite_sheet('arrows.png', 69, 100, -1)
        arrows_rev = []
        for arrow in arrows:
            image = arrow.copy()
            image = pygame.transform.flip(image, True, False)
            arrows_rev.append(image)
        
        self.next_btn = TogglableImageButton(self, arrows, callback = self.next_page_click)
        self.prev_btn = TogglableImageButton(self, arrows_rev, callback = self.prev_page_click)
        
        self.back_btn = BasicTextButton(self, text='< Back to Main Menu', callback = parent.main_menu_click, font = self.font)
        
    def build_from_mission_list(self, missions = None):
        '''build the mission list using the list of mission...'''
        if missions:
            self.missions = missions
        
        n = 0
        for mission in self.missions:
            # add a button to the child list for each mission
            n += 1
            
            self.add_child(BasicImageButton(self, image = mission[1], select_fxn = self.mouse_over_callback, unselect_fxn = self.mouse_off_callback, callback = self.mission_click, callback_kwargs = {'mission':mission}))
    
    def update(self, event):
        #super(MissionMenu, self).update(event)
        num_pages = self.get_num_pages()
        
        if self.page < 1: self.page = 1
        if self.page > num_pages: self.page = num_pages
        
        start_i = (self.page - 1) * self.num_per_page
        end_i = self.page * self.num_per_page
        if end_i > len(self.missions): end_i = len(self.missions)
        
        for i in range(start_i, end_i):
            self.children[i].update(event)
        
        if len(self.children) > len(self.missions):
            for i in range(len(self.missions), len(self.children)):
                self.children[i].update(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()
    
    def get_num_pages(self):
        num_pages = len(self.missions) / float(self.num_per_page)
        if num_pages > int(num_pages): num_pages = int(num_pages) + 1
        return num_pages
    
    def draw(self):
        '''draws the mission selection screen'''
        screen = pygame.display.get_surface()
        num_pages = self.get_num_pages()
        
        if self.page < 1: self.page = 1
        if self.page > num_pages: self.page = num_pages
        
        # enable/disable prev page button
        if self.page > 1 and not self.prev_btn.is_enabled(): 
            self.prev_btn.set_enabled(True)
        elif self.prev_btn.is_enabled() and self.page <= 1:
            self.prev_btn.set_enabled(False)
            
        # enable/disable next page button
        if self.page < num_pages and not self.next_btn.is_enabled(): 
            self.next_btn.set_enabled(True)
        elif self.next_btn.is_enabled() and self.page >= num_pages:
            self.next_btn.set_enabled(False)
        
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
            y = draw_rect.top + (draw_rect.height - child.image.get_rect().height) * 0.5
            child.rect.topleft = (x, y)
            child.draw()
            x += child.rect.width + self.h_pad
        
        # draw the prev/next buttons
        x = draw_rect.left - self.prev_btn.rect.width - self.h_pad
        y = draw_rect.top + (draw_rect.height - self.prev_btn.rect.height) * 0.5
        self.prev_btn.rect.topleft = (x, y)
        self.prev_btn.draw()
        
        x = draw_rect.left + draw_rect.width + self.h_pad
        y = draw_rect.top + (draw_rect.height - self.next_btn.rect.height) * 0.5
        self.next_btn.rect.topleft = (x, y)
        self.next_btn.draw()
        
        # draw the back to main menu button
        x = (screen.get_width() - self.desc_max_width) * 0.5
        y = draw_rect.top - self.v_pad * 3 - self.back_btn.rect.height
        self.back_btn.rect.topleft = (x, y)
        self.back_btn.draw()
        
        # draw the mission info
        if self.selected_mission:
            y = draw_rect.top + draw_rect.height + self.v_pad * 3
            size = self.font.size(self.selected_mission[2])
            x = (screen.get_width() - size[0]) * 0.5
            screen.blit(self.font.render(self.selected_mission[2], 1, self.title_color), (x, y))
            
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
            
        
    def mouse_over_callback(self, child):
        self.selected_mission = child.callback_kwargs.get('mission', None)
        
    def mouse_off_callback(self, child):
        if self.selected_mission is child.callback_kwargs.get('mission', None): self.selected_mission = None
    
    def mission_click(self, **kwargs):
        mission = kwargs.get('mission', None)
        self.parent.close()
        if mission and self.mission_start and mission in self.missions:
            self.mission_start(mission)
        
    def next_page_click(self, **kwargs):
        self.page += 1
    
    def prev_page_click(self, **kwargs):
        self.page -= 1
    
