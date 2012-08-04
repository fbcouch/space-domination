'''
Created on Jun 13, 2012

@author: Jami
'''
from pygame.locals import *
from simplemenuclass.menu import cMenu, EVENT_CHANGE_STATE
import math
import os
import pygame
import random
import sys

MENU_MAIN = 0 # 0-99 reserved for menu pages
MENU_OPTIONS = 1
MENU_PAUSE = 2
MENU_MISSION_SELECT = 3
MENU_EXIT = 100 # 100-199 reserved for actions
MENU_RESUME = 101
MENU_MISSION = 200 # missions will start with 2xx with xx being mission ID
EVENT_CHANGE_STATE = pygame.USEREVENT + 1

class Menu(object):
    x_offset = 0
    y_offset = 0
    h_pad = 0
    v_pad = 0
    orientation = 'vertical'
    num_per_rowcol = 0
    background = None
    draw_surface = None
    button_list = None
    font = None
    
    centered = False
    centered_on_screen = False
    
    h_align = 'left'
    v_align = 'top'
    
    selected_color = None
    unselected_color = None
    
    selected_btn = None
    
    def __init__(self, x_offset, y_offset, h_pad = 0, v_pad = 0, orientation = 'vertical', number = 10, background = None, button_list = None):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.h_pad = h_pad
        self.v_pad = v_pad
        self.orientation = orientation
        self.num_per_rowcol = number
        self.background = background.copy()
        self.draw_surface = background
        self.button_list = []
        
        
        
        self.font = pygame.font.Font(None, 32)
        
        self.selected_color = (255, 0, 0)
        self.unselected_color = (255, 255, 255)
        
        
        for button in button_list:
            self.button_list.append(self.create_button(button))
            
        if len(self.button_list) > 0:
            selected_btn = self.button_list[0]
        
    def create_button(self, info):
        return_btn = {'text': info[0], 'state': info[1], 'image': info[2], 
                      'selected-image': None, 'unselected-image': None, 
                      'collide-rect': None}
        
        # create images for "selected", "unselected"
        if info[2]: 
            # we have an image - create a rectangle in the selected color
            return_btn['unselected-image'] = return_btn['image'].copy()
            temp_image = pygame.surface.Surface(
                                    (return_btn['image'].get_width() + 4, 
                                     return_btn['image'].get_height() + 4))
            temp_image.blit(return_btn['image'], (2,2))
            pygame.gfxdraw.box(temp_image, 
                               pygame.rect.Rect(0, 0, 
                                                temp_image.get_width(), 
                                                temp_image.get_height()), 
                               self.selected_color)
            pygame.gfxdraw.box(temp_image, 
                               pygame.rect.Rect(1, 1, 
                                                temp_image.get_width() - 2, 
                                                temp_image.get_height() - 2), 
                               self.selected_color)
            return_btn['selected-image'] = temp_image
        else: # no image, use text
            if not return_btn['text']:
                return_btn['text'] = "Default Button"
            return_btn['selected-image'] = self.font.render(return_btn['text'],
                                                        1, 
                                                        self.selected_color)
            return_btn['unselected-image'] = self.font.render(
                                                      return_btn['text'], 1, 
                                                      self.unselected_color)
            
        return return_btn
        
    def redraw_all(self):
        pass
    
    def draw_buttons(self, draw_surface = None):
        if draw_surface:
            self.draw_surface = draw_surface
            
        
        # TODO implement centered and centered_on_screen
        y = self.y_offset
        for button in self.button_list:
            if button is self.selected_btn:
                self.draw_surface.blit(button['selected-image'], (self.x_offset, y))
            else:
                self.draw_surface.blit(button['unselected-image'], (self.x_offset, y))
            y += button['unselected-image'].get_height() + self.v_pad
        
    
    def update(self, event, state):
        if event.type == pygame.KEYDOWN:
            sel_item = self.button_list.index(self.selected_btn)
            if event.key == pygame.K_UP:
                if self.orientation == 'vertical':
                    if sel_item > 0:
                        sel_item -= 1
                    else:
                        sel_item = len(self.button_list) - 1                
                else:
                    pass
            elif event.key == pygame.K_DOWN:
                if self.orientation == 'vertical':
                    if sel_item < len(self.button_list) - 1:
                        sel_item += 1
                    else:
                        sel_item = 0
                else:
                    pass
            elif event.key == pygame.K_LEFT:
                if self.orientation == 'vertical':
                    pass
                else:
                    pass
            elif event.key == pygame.K_RIGHT:
                if self.orientation == 'vertical':
                    pass
                else:
                    pass
            elif event.key == pygame.K_RETURN:
                state = self.selected_btn['state']
                
            self.selected_btn = self.button_list[sel_item]  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass #TODO implement mouse listening for the menu
        elif event.type == EVENT_CHANGE_STATE:
            if len(self.button_list) > 0:
                self.selected_btn = self.button_list[0]
        
        
        return state
    
    def set_center(self, centered = False, centered_on_screen = False):
        self.centered = centered
        self.centered_on_screen = centered_on_screen
    
    def set_alignment(self, h_align = 'left', v_align = 'top'):
        if h_align in ['left', 'center', 'right']:
            self.h_align = h_align
        if v_align in ['top', 'center', 'bottom']:
            self.v_align = v_align

class MenuManager(object):
    menuList = None
    selectedMenu = 0 # default to no menu shown
    screen = None
    parent = None
    
    def __init__(self, screen = None, parent = None):
        self.menuList = []
        self.screen = screen
        self.parent = parent
        
        
        
        
        # menu 0 = main menu
        self.menuList.append(Menu(50, 50, 20, 5, 'vertical', 100, screen,
                                   [('Select Mission', MENU_MISSION_SELECT, None),
                                    ('Options', MENU_OPTIONS, None),
                                    ('Exit', MENU_EXIT, None)]))
        
        # menu 1 = options menu
        self.menuList.append(cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                                   [('Back', MENU_MAIN, None)]))
        
        # menu 2 = pause menu
        self.menuList.append(cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                                [('Resume', MENU_RESUME, None),
                                 ('Options', MENU_OPTIONS, None),
                                 ('Exit', MENU_EXIT, None)]))
        # menu 3 = mission menu
        mlist = []
        i = 0
        for mission in self.parent.missionList:
            mlist.append(['', 200 + i, mission[1]])
            
            i += 1
            
        self.menuList.append(cMenu(50, 50, 50, 5, 'horizontal', 4, screen, mlist))
            
        return
    
    def draw(self):
        self.menuList[self.selectedMenu].redraw_all()
        self.menuList[self.selectedMenu].draw_buttons()
    
    def update(self, event = None):
        state = self.menuList[self.selectedMenu].update(event, self.selectedMenu)    
        if state != self.selectedMenu: self.menu_state_parse(state)
        
    
    def menu_state_parse(self, state = 0):
        if(state == MENU_MAIN):
            self.selectedMenu = MENU_MAIN
        elif(state == MENU_RESUME):
            self.selectedMenu = -1
        elif(state == MENU_EXIT):
            sys.exit(0)
        elif(state == MENU_OPTIONS):
            self.selectedMenu = MENU_OPTIONS
        elif(state == MENU_PAUSE):
            self.selectedMenu = MENU_PAUSE
        elif(state == MENU_MISSION_SELECT):
            self.selectedMenu = MENU_MISSION_SELECT
        elif(state >= MENU_MISSION):
            # mission selected
            self.parent.currentMission = self.parent.loadMission(
                                     self.parent.missionList[state - 200][0])
            self.parent.buildMission(self.parent.currentMission)
            self.parent.gameState = self.parent.GAMESTATE_PAUSED
            self.selectedMenu = MENU_PAUSE
        
        self.menuList[self.selectedMenu].set_alignment('center', 'center')
        self.menuList[self.selectedMenu].set_center(True, True)  
        self.menuList[self.selectedMenu].update(
                            pygame.event.Event(EVENT_CHANGE_STATE, key = 0),
                            self.selectedMenu)
        
        
        return self.selectedMenu
    
    def is_active(self):
        if self.selectedMenu >= 0 and self.selectedMenu < len(self.menuList):
            return True
        else:
            return False