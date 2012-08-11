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

class Button(object):
    '''basic button in the old style for menus'''

    attrs = None
    font = None
    selected_color = None
    unselected_color = None
    
    def __init__(self, text, state, image, font = None, selected_color = None, unselected_color = None):
        
        if not font:
            self.font = pygame.font.Font(None, 20)
        else:
            self.font = font
        
        self.selected_color = selected_color
        if not self.selected_color: self.selected_color = (250, 0, 0)
        self.unselected_color = unselected_color
        if not self.unselected_color: self.unselected_color = (250, 250, 250)
        
        self.attrs = self.create_button([text, state, image])

    def create_button(self, info):
        '''create a button from @param info, a tuple containing (text, state, image)'''
        return_btn = {'text': info[0], 'state': info[1], 'image': info[2], 
                      'selected-image': None, 'unselected-image': None, 
                      'collide-rect': None}
        
        # create images for "selected", "unselected"
        if return_btn['image']: 
            # we have an image - create a rectangle in the selected color
            return_btn['unselected-image'] = return_btn['image']
            temp_image = pygame.surface.Surface(
                                    (return_btn['image'].get_width() + 4, 
                                     return_btn['image'].get_height() + 4))
            temp_image.blit(return_btn['image'], (2,2))
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            pygame.gfxdraw.rectangle(temp_image, 
                               pygame.rect.Rect(0, 0, 
                                                temp_image.get_width(), 
                                                temp_image.get_height()), 
                               self.selected_color)
            pygame.gfxdraw.rectangle(temp_image, 
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
    
    
    def draw(self, draw_surface, x, y, width, height, centered, selected):
        '''draw the button to @param draw_surface in the box defined by @param x, @param y, @param width, @param height'''
        draw_x = x
        draw_y = y
        if selected:
            if centered:
                draw_x = x + (width - self.attrs['selected-image'].get_width()) * 0.5
                draw_y = y + (height - self.attrs['selected-image'].get_height()) * 0.5
            draw_surface.blit(self.attrs['selected-image'], (draw_x, draw_y))
            self.attrs['collide-rect'] = self.attrs['selected-image'].get_rect(topleft=(draw_x,draw_y))
        else:
            if centered:
                draw_x = x + (width - self.attrs['unselected-image'].get_width()) * 0.5
                draw_y = y + (height - self.attrs['unselected-image'].get_height()) * 0.5
            draw_surface.blit(self.attrs['unselected-image'], (draw_x, draw_y))
            self.attrs['collide-rect'] = self.attrs['unselected-image'].get_rect(topleft=(draw_x,draw_y))
        
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
    
    def __init__(self, x_offset = 0, y_offset = 0, h_pad = 0, v_pad = 0, orientation = 'vertical', number = 10, background = None, button_list = None):
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
            self.button_list.append(Button(button[0], button[1], button[2], self.font, self.selected_color, self.unselected_color))
            
        if len(self.button_list) > 0:
            selected_btn = self.button_list[0]
        
    def redraw_all(self):
        pass
    
    def draw_buttons(self, draw_surface = None):
        if draw_surface:
            self.draw_surface = draw_surface
        
        bounding_rect = pygame.rect.Rect(0,0,0,0) # we need to find the dimensions we'll need to draw the menu...
        
        y = 0
        x = 0
        row = 0
        col = 0
        col_widths = []
        row_heights = []
        for button in self.button_list:
            button = button.attrs
            if self.orientation == 'vertical':
                if row >= self.num_per_rowcol:
                    row = 0
                    x += col_widths[col] + self.h_pad
                    col += 1
                    col_widths.append(0)

                y += button['unselected-image'].get_height()
                if row > 0: y += self.v_pad
                
                if col >= len(col_widths):
                    col_widths.append(button['unselected-image'].get_width())
                elif button['unselected-image'].get_width() > col_widths[col]:
                    col_widths[col] = button['unselected-image'].get_width()
                
                if col == 0:
                    row_heights.append(button['unselected-image'].get_height())
                elif button['unselected-image'].get_height() > row_heights[row]:
                    row_heights[row] = button['unselected-image'].get_height()
                row += 1
            
            else:
                if col >= self.num_per_rowcol:
                    col = 0
                    y += row_heights[row] + self.v_pad
                    row += 1
                    row_heights.append(0)
                
                x += button['unselected-image'].get_width()
                if col > 0: x += self.h_pad
                
                
                if row >= len(row_heights):
                    row_heights.append(button['unselected-image'].get_height())
                elif button['unselected-image'].get_height > row_heights[row]:
                    row_heights[row] = button['unselected-image'].get_height()
                
                if row == 0:
                    col_widths.append(button['unselected-image'].get_width())
                elif button['unselected-image'].get_width() > col_widths[col]:
                    col_widths[col] = button['unselected-image'].get_width()
                
                col += 1
            
            
        if self.orientation == 'vertical':
            x += col_widths[col]
        else:
            y += row_heights[row]
        
        bounding_rect.width = x
        bounding_rect.height = y
        
        
        row = 0
        col = 0
        if self.centered_on_screen:
            x = (self.draw_surface.get_width() - bounding_rect.width) * 0.5
            y = (self.draw_surface.get_height() - bounding_rect.height) * 0.5
        else:
            x = self.x_offset
            y = self.y_offset
        bounding_rect.left = x
        bounding_rect.top = y
        for button in self.button_list:
            if self.orientation == 'vertical':
                if row >= self.num_per_rowcol:
                    row = 0
                    x += col_widths[col] + self.h_pad
                    col += 1
                
                button.draw(self.draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                
                y += button.attrs['unselected-image'].get_height() + self.v_pad
                row += 1
            
            else:
                if col >= self.num_per_rowcol:
                    col = 0
                    y += row_heights[row] + self.v_pad
                    row += 1
                
                button.draw(self.draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                
                x += button.attrs['unselected-image'].get_width() + self.h_pad
                col += 1
        
        #pygame.gfxdraw.rectangle(self.draw_surface, bounding_rect, (255,255,255))
    
    def draw_button(self, button, x, y, width, height):
        draw_x = x
        draw_y = y             
        
        if button is self.selected_btn:
            
            if self.centered:
                draw_x = x + (width - button['selected-image'].get_width()) * 0.5
                draw_y = y + (height - button['selected-image'].get_height()) * 0.5
            self.draw_surface.blit(button['selected-image'], (draw_x, draw_y))
            button['collide-rect'] = button['selected-image'].get_rect(topleft=(draw_x,draw_y))
        else:
            if self.centered:
                draw_x = x + (width - button['unselected-image'].get_width()) * 0.5
                draw_y = y + (height - button['unselected-image'].get_height()) * 0.5
            self.draw_surface.blit(button['unselected-image'], (draw_x, draw_y))
            button['collide-rect'] = button['unselected-image'].get_rect(topleft=(draw_x,draw_y))
    
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
                    if sel_item > 0:
                        sel_item -= 1
                    else:
                        sel_item = len(self.button_list) - 1
            elif event.key == pygame.K_RIGHT:
                if self.orientation == 'vertical':
                    pass
                else:
                    if sel_item < len(self.button_list) - 1:
                        sel_item += 1
                    else:
                        sel_item = 0
                        
            elif event.key == pygame.K_RETURN:
                state = self.selected_btn.attrs['state']
                
            self.selected_btn = self.button_list[sel_item]  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.button_list:
                    if button.attrs['collide-rect'].collidepoint(event.pos):
                        self.selected_btn = button
            print "MOUSEBUTTONDOWN: (btn %s, pos %s)" % (event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.selected_btn.attrs['collide-rect'].collidepoint(event.pos):
                    state = self.selected_btn.attrs['state']
            print "MOUSEBUTTONUP: (btn %s, pos %s)" % (event.button, event.pos)
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
        self.menuList.append(Menu(50, 50, 20, 5, 'vertical', 100, screen,
                                   [('Back', MENU_MAIN, None)]))
        
        # menu 2 = pause menu
        self.menuList.append(Menu(50, 50, 20, 5, 'vertical', 100, screen,
                                [('Resume', MENU_RESUME, None),
                                 ('Options', MENU_OPTIONS, None),
                                 ('Exit', MENU_EXIT, None)]))
        # menu 3 = mission menu
        mlist = []
        i = 0
        for mission in self.parent.missionList:
            mlist.append(['', 200 + i, mission[1]])
            
            i += 1
            
        self.menuList.append(Menu(50, 50, 50, 5, 'horizontal', 4, screen, mlist))
            
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