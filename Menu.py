'''
Created on Jun 13, 2012

@author: Jami
'''
from profile import Profile
from pygame.locals import *
from simplemenuclass.menu import cMenu, EVENT_CHANGE_STATE
import Utils
import math
import os
import pygame
import random
import sys
import traceback

MENU_MAIN = 0 # 0-99 reserved for menu pages
MENU_OPTIONS = 1
MENU_PAUSE = 2
MENU_MISSION_SELECT = 3
MENU_SHIP_SELECT = 4
MENU_PROFILE = 5
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
    
    on_click_fxn = None
    
    def __init__(self, text, state, image, font = None, selected_color = None, unselected_color = None, on_click_fxn = None):
        
        if not font:
            self.font = pygame.font.Font(None, 20)
        else:
            self.font = font
        
        self.selected_color = selected_color
        if not self.selected_color: self.selected_color = (250, 0, 0)
        self.unselected_color = unselected_color
        if not self.unselected_color: self.unselected_color = (250, 250, 250)
        
        self.attrs = self.create_button([text, state, image])
        self.on_click_fxn = on_click_fxn

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
        
    def on_click(self):
        '''called when the button is clicked or return is pressed while selected'''
        if self.on_click_fxn:
            return self.on_click_fxn()
    
    def on_selected(self):
        '''called when the button is selected'''
        
    def on_keypress(self, key, mod):
        '''called when a key that is not normally handled by the menu is pressed'''

class MissionButton(Button):
    '''special button specifically for missions'''
    
    mission = None
    mission_start = None
    
    def __init__(self, context, text, mission, image, font = None, selected_color = None, unselected_color = None):
        '''rather than a "state", which this button will always set to -1, this has a Mission'''
        super(MissionButton, self).__init__(text, -1, image, font, selected_color, unselected_color)
        self.mission = mission
        self.mission_start = context.startMission
        
    def on_click(self):
        self.mission_start(self.mission)
        return self.attrs['state']
    
class ShipButton(Button):
    '''special button for selecting ships'''
    ship = None
    context = None
    
    def __init__(self, context, text, state, ship, image, font = None, selected_color = None, unselected_color = None):
        super(ShipButton, self).__init__(text, state, image, font, selected_color, unselected_color)
        self.ship = ship
        self.context = context
    
    def on_click(self):
        self.context.currentProfile['ship'] = self.ship.id
        return self.attrs['state']

class SaveButton(Button):
    '''this button calls "on_click" for all other items in the parent before its own'''
    parent = None
    def __init__(self, parent, text, state, image, font = None, selected_color = None, unselected_color = None, on_click_fxn = None):
        super(SaveButton, self).__init__(text, state, image, font, selected_color, unselected_color, on_click_fxn)
        self.parent = parent
    
    def on_click(self):
        for item in self.parent.button_list:
            if not item is self:
                item.on_click()
        super(SaveButton, self).on_click()
        
class TextInput(Button):
    '''special button used for text input'''
    
    label = ""
    value = ""
    numbers_only = False
    
    link = None # a tuple containing (var, key) such that var[key] will be set to self.value on click
    
    keymap = {K_0: '0', K_1: '1', K_2: '2', K_3: '3', K_4: '4', K_5: '5', K_6: '6', K_7: '7', K_8: '8', K_9: '9',
              K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e', K_f: 'f', K_g: 'g', K_h: 'h', K_i: 'i', K_j: 'j', 
              K_k: 'k', K_l: 'l', K_m: 'm', K_n: 'n', K_o: 'o', K_p: 'p', K_q: 'q', K_r: 'r', K_s: 's', K_t: 't', 
              K_u: 'u', K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y', K_z: 'z', K_MINUS: '-', K_UNDERSCORE: '_'}
    numbers = {K_0: '0', K_1: '1', K_2: '2', K_3: '3', K_4: '4', K_5: '5', K_6: '6', K_7: '7', K_8: '8', K_9: '9'}
    
    def __init__(self, label, value, state, font = None, selected_color = None, unselected_color = None, numbers_only = False, link = None):
        self.label = str(label)
        self.value = str(value)
        
        super(TextInput, self).__init__((self.label + ": " + self.value), state, None, font, selected_color, unselected_color)
        self.numbers_only = numbers_only
        self.link = link
        self.update_images()
        
    def on_keypress(self, key, mod):
        print "keypress (%s, %s)" % (str(key), str(mod))
        
        if key in self.numbers or (not self.numbers_only and key in self.keymap):
            if pygame.K_LSHIFT & mod or pygame.K_RSHIFT & mod:
                self.value += self.keymap[key].capitalize()
            else:
                self.value += self.keymap[key]
        elif key == pygame.K_BACKSPACE:
            if len(self.value) > 0:
                self.value = self.value[:len(self.value) - 1]
                
        self.update_images()
        
    def update_images(self):
        self.attrs['unselected-image'] = self.font.render(self.label + ": " + self.value, 1, self.unselected_color)
        self.attrs['selected-image'] = self.font.render(self.label + ": " + self.value + "_", 1, self.selected_color)
        
    def on_click(self):
        if self.link:
            self.link[0][self.link[1]] = self.value
        
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
    
    centered = True
    centered_on_screen = True
    
    h_align = 'center'
    v_align = 'center'
    
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
        if background:
            self.background = background.copy()
        else:
            self.background = None
        self.draw_surface = background
        self.button_list = []
        
        
        
        self.font = pygame.font.Font(None, 32)
        
        self.selected_color = (255, 0, 0)
        self.unselected_color = (255, 255, 255)
        
        
        if not button_list: button_list = []
        for button in button_list:
            self.add_button(button)
            
        if len(self.button_list) > 0:
            self.selected_btn = self.button_list[0]
    
    def add_button(self, button):
        if isinstance(button, Button): self.button_list.append(button)
        else: self.button_list.append(Button(button[0], button[1], button[2], self.font, self.selected_color, self.unselected_color))
        
        if not self.selected_btn:
            self.selected_btn = self.button_list[len(self.button_list) - 1]
        
    def redraw_all(self):
        pass
    
    def draw_buttons(self, draw_surface = None):
        if draw_surface:
            self.draw_surface = draw_surface
        
        if len(self.button_list) == 0:
            return
        
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
                    y = 0

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
                    x = 0
                
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
        
        x = -1 * self.h_pad
        for c in col_widths:
            x += c + self.h_pad
        bounding_rect.width = x
        y = -1 * self.v_pad
        for r in row_heights:
            y += r + self.v_pad
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
        x_start = x
        y_start = y
        for button in self.button_list:
            if self.orientation == 'vertical':
                if row >= self.num_per_rowcol:
                    row = 0
                    x += col_widths[col] + self.h_pad
                    col += 1
                    y = y_start
                
                button.draw(self.draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                
                y += button.attrs['unselected-image'].get_height() + self.v_pad
                row += 1
            
            else:
                if col >= self.num_per_rowcol:
                    col = 0
                    y += row_heights[row] + self.v_pad
                    row += 1
                    x = x_start
                
                button.draw(self.draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                
                x += button.attrs['unselected-image'].get_width() + self.h_pad
                col += 1
                
        return bounding_rect
        
    
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
                self.selected_btn.on_click()
            
            elif event.key == pygame.K_ESCAPE:
                state = MENU_MAIN
                
            else:
                self.selected_btn.on_keypress(event.key, event.mod)
            
            if not self.selected_btn == self.button_list[sel_item]:    
                self.selected_btn = self.button_list[sel_item]
                self.selected_btn.on_selected()  
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.button_list:
                    if button.attrs['collide-rect'].collidepoint(event.pos):
                        self.selected_btn = button
            #print "MOUSEBUTTONDOWN: (btn %s, pos %s)" % (event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.selected_btn.attrs['collide-rect'].collidepoint(event.pos):
                    state = self.selected_btn.attrs['state']
                    self.selected_btn.on_click()
            #print "MOUSEBUTTONUP: (btn %s, pos %s)" % (event.button, event.pos)
        #elif event.type == EVENT_CHANGE_STATE:
        #    if len(self.button_list) > 0:
        #        self.selected_btn = self.button_list[0]
        
        
        return state
    
    def set_center(self, centered = False, centered_on_screen = False):
        self.centered = centered
        self.centered_on_screen = centered_on_screen
    
    def set_alignment(self, h_align = 'left', v_align = 'top'):
        if h_align in ['left', 'center', 'right']:
            self.h_align = h_align
        if v_align in ['top', 'center', 'bottom']:
            self.v_align = v_align

class PagedMenu(Menu):
    '''this menu will be a horizontal layout with an up and down arrow to change pages when the number of items > num_per_rowcol'''
    full_button_list = None
    dot_size = 10
    
    def __init__(self, x_offset = 0, y_offset = 0, h_pad = 0, v_pad = 0, number = 10, background = None, button_list = None):
        super(PagedMenu, self).__init__(x_offset, y_offset, h_pad, v_pad, 'horizontal', number, background, button_list)
        self.full_button_list = []
        for btn in self.button_list:
            self.full_button_list.append(btn)
        
    def add_button(self, button):
        super(PagedMenu, self).add_button(button)
        self.full_button_list.append(self.button_list[len(self.button_list) - 1])
        
    def draw_buttons(self, draw_surface = None):
        if not draw_surface:
            draw_surface = self.draw_surface
        else:
            self.draw_surface = draw_surface
        
        # get the page based on the int val of selected index / num per rowcol
        page = int(self.full_button_list.index(self.selected_btn) / self.num_per_rowcol)
        max_page = int(len(self.full_button_list) / self.num_per_rowcol)
        
        # select the proper subset to draw
        if page < max_page:
            self.button_list = self.full_button_list[int(page * self.num_per_rowcol):int((page + 1) * self.num_per_rowcol)]
        if page == max_page:
            self.button_list = self.full_button_list[int(page * self.num_per_rowcol):]
        
        # draw
        menu_rect = super(PagedMenu, self).draw_buttons(draw_surface)
        
        # restore the button list
        self.button_list = self.full_button_list
        
        # draw the page numbers
        dots_width = -1 * self.dot_size
        for p in range(0, max_page + 1):
            dots_width += self.dot_size * 2
        
        dots_width = max_page * self.dot_size + (max_page + 1) * self.dot_size + 1
        dots_surf = pygame.surface.Surface((dots_width, self.dot_size))
        dots_surf.set_colorkey((0,0,0))
        x = int(self.dot_size * 0.5)
        for p in range(0, max_page + 1):
            if p == page:
                pygame.gfxdraw.filled_circle(dots_surf, x, int(self.dot_size * 0.5), int(self.dot_size * 0.5), self.selected_color)
            else:
                pygame.gfxdraw.filled_circle(dots_surf, x, int(self.dot_size * 0.5), int(self.dot_size * 0.5), self.unselected_color)
            x += self.dot_size * 2
            
        if self.centered_on_screen:
            draw_x = (draw_surface.get_width() - dots_width) * 0.5
        else:
            draw_x = self.x_offset
        
        draw_y = menu_rect.top + menu_rect.height + self.v_pad * 2
        
        self.draw_surface.blit(dots_surf, (draw_x, draw_y))

class ProfileMenu(Menu):
    # contains the profile list from the parent
    profile_list = None
    # contains a reference to the save profiles function
    profile_save = None
    # contains a reference to a "set active profile" function
    profile_set = None
    
    mode = 'view'
    
    new_profile = None
    
    profile = None
    current_active = None
    
    fonts = None
    
    ship_selector = None
    
    ticks = 0
    
    context = None
    
    def __init__(self, context, draw_surface = None):
        super(ProfileMenu, self).__init__()
        
        self.context = context
        self.profile_list = context.profiles
        self.profile_save = context.saveProfiles
        self.profile_set = context.setActiveProfile
        if not draw_surface:
            draw_surface = pygame.display.get_surface()
        self.draw_surface = draw_surface
        self.profile = context.currentProfile
        self.current_active = context.currentProfile
        
        
        self.fonts = {}
        self.fonts['small'] = pygame.font.Font(None, 16)
        self.fonts['medium'] = pygame.font.Font(None, 20)
        self.fonts['large'] = pygame.font.Font(None, 28)
        
        self.set_profile_view()
    
        menu = PagedMenu(50, 50, 50, 50, 4, draw_surface, [])
        for ship in context.shipList:
            if ship.player_flyable:
                image, rect = Utils.load_image(ship.file, -1)
                image = pygame.transform.rotate(image, 90)
                menu.add_button(Button('', ship.id, image, menu.font, menu.selected_color, menu.unselected_color))
        if len(menu.button_list) > 0:
            menu.selected_btn = menu.button_list[0]
        self.ship_selector = menu
         
    def set_profile_view(self):
        '''this class sets up the profile view buttons'''
        self.button_list = []
        self.button_list.append(Button('Change Profile', 'select', None, self.font, self.selected_color, self.unselected_color))
        self.button_list.append(Button('Edit Profile', 'edit', None, self.font, self.selected_color, self.unselected_color))
        self.button_list.append(Button('New Profile', 'new', None, self.font, self.selected_color, self.unselected_color))
        self.button_list.append(Button('Delete Profile', 'delete', None, self.font, self.selected_color, self.unselected_color))
        self.button_list.append(Button('Main Menu', MENU_MAIN, None, self.font, self.selected_color, self.unselected_color))
        self.mode = 'view'
        self.orientation = 'horizontal'
        self.set_alignment('left', 'top')
        self.set_center(False, False)
        self.h_pad = 20
        self.selected_btn = self.button_list[0]
        
    def set_profile_select(self):
        '''this class sets up the profile selection menu'''
        self.button_list = []
        for profile in self.profile_list:
            button = Button(profile['name'], profile, None, self.font, self.selected_color, self.unselected_color)
            self.button_list.append(button)
            if len(self.button_list) == 1: self.selected_btn = self.button_list[0]
            if profile is self.profile:
                self.selected_btn = button
        self.button_list.append(Button('Cancel', 'cancel', None, self.font, self.selected_color, self.unselected_color))
        self.mode = 'select'
        self.orientation = 'vertical'
        self.set_alignment('left', 'center')
        self.set_center(False, True)
        self.h_pad = 20
        self.v_pad = 20
    
    def set_ship_select(self):
        self.mode = 'ship-select'
        if 'ship' in self.profile:            
            for btn in self.ship_selector.button_list:
                if int(self.profile['ship']) == btn.attrs['state']:
                    self.ship_selector.selected_btn = btn
        else:
            if len(self.ship_selector.button_list) > 0:
                self.ship_selector.selected_btn = self.ship_selector.button_list[0]
        self.ship_selector.set_alignment('center','center')
        self.ship_selector.set_center(True, True)
        
    def set_profile_edit(self):
        '''this class sets up the profile edit menu'''
        self.button_list = []
        self.add_button(TextInput('Callsign', self.profile['name'], 'none', self.font, self.selected_color, self.unselected_color, False, (self.profile, 'name')))
        self.add_button(TextInput('Width', self.profile['width'], 'none', self.font, self.selected_color, self.unselected_color, True, (self.profile, 'width')))
        self.add_button(TextInput('Height', self.profile['height'], 'none', self.font, self.selected_color, self.unselected_color, True, (self.profile, 'height')))
        self.add_button(('Select Ship...', 'ship-select', None))
        self.add_button(Button('Save', 'save', None, self.font, self.selected_color, self.unselected_color))
        self.add_button(('Cancel', 'cancel', None))
        self.selected_btn = self.button_list[0]
        self.mode = 'edit'
        self.orientation = 'vertical'
        self.set_alignment('left', 'center')
        self.set_center(False, True)
        self.h_pad = 20
        self.v_pad = 20
    
    def set_profile_new(self):
        '''this class sets up the profile new menu'''
        self.button_list = []
        self.add_button(TextInput('Callsign', 'newbie', 'none', self.font, self.selected_color, self.unselected_color, False, (self.profile, 'name')))
        self.add_button(Button('Save', 'save', None, self.font, self.selected_color, self.unselected_color))
        self.add_button(('Cancel', 'cancel', None))
        self.selected_btn = self.button_list[0]
        self.mode = 'new'
        self.orientation = 'vertical'
        self.set_alignment('left', 'center')
        self.set_center(False, True)
        self.h_pad = 20
        self.v_pad = 20
        
    def set_profile_remove(self):
        '''this class sets up the profile removal confirmation'''
        self.button_list = []
        self.add_button(Button('Confirm Delete of Profile: %s' % self.profile['name'], 'delete', None, self.font, self.selected_color, self.unselected_color))
        self.add_button(Button('Cancel', 'cancel', None, self.font, self.selected_color, self.unselected_color))
        self.selected_btn = self.button_list[0]
        self.mode = 'delete'
        self.orientation = 'vertical'
        self.set_alignment('left', 'center')
        self.set_center(True, True)
        self.h_pad = 20
        self.v_pad = 5
        
    def update(self, event, state):
        if self.mode == 'ship-select':
            new_state = self.ship_selector.update(event, state)
            if new_state == state:
                return state
        else:
            new_state = super(ProfileMenu, self).update(event, state)
        
        if isinstance(new_state, Profile):
            if self.mode == 'select':
                self.profile = new_state
                self.set_profile_view()
        elif new_state == 'save':
            for btn in self.button_list:
                if btn.attrs['state'] == 'save':
                    break
                btn.on_click()
            
            if self.mode == 'new':
                
                id = -1
                for pf in self.profile_list:
                    if int(pf['id']) > id:
                        id = int(pf['id'])
                id += 1
                self.profile['id'] = id
                self.profile['width'] = pygame.display.get_surface().get_width()
                self.profile['height'] = pygame.display.get_surface().get_height()
                self.profile_list.append(self.profile)
                self.set_profile_edit()
            else:
                self.set_profile_view()
            self.profile_set(self.profile)
            self.profile_save()
        elif new_state == 'edit':
            self.set_profile_edit()
        elif new_state == 'new':
            self.profile = Profile()
            self.set_profile_new()
        elif new_state == 'view':
            self.set_profile_view()
        elif new_state == 'select':
            self.profile_set(self.profile)
            self.current_active = self.profile
            self.set_profile_select()
            self.profile_save()
        elif new_state == 'cancel':
            if self.mode == 'ship-select':
                self.set_profile_edit()
            else:
                self.profile = self.current_active
                self.set_profile_view()
        elif new_state == 'ship-select':
            self.set_ship_select()
        elif new_state == 'delete':
            if self.mode == 'delete':
                # really delete
                if self.profile in self.profile_list: 
                    print "removing %s" % self.profile['name']
                    self.profile_list.remove(self.profile)
                if len(self.profile_list) > 0:
                    self.context.currentProfile = self.profile_list[0]
                else:
                    self.context.currentProfile = Profile()
                
                self.profile = self.context.currentProfile
                self.current_active = self.context.currentProfile
                self.profile_save()
                self.set_profile_view()
            else:
                self.set_profile_remove()
                
        elif new_state == 'none':
            pass
        else:
            if self.mode == 'ship-select':
                self.profile['ship'] = new_state
                self.set_profile_edit()
            else:
                state = new_state
        return state
    
    def draw_buttons(self, draw_surface = None):
        self.ticks += 1
        if draw_surface:
            self.draw_surface = draw_surface
        
        
        image, draw_rect = Utils.load_image('profile-back.png', -1)
        draw_rect.topleft = ((self.draw_surface.get_width() - draw_rect.width) * 0.5, (self.draw_surface.get_height() - draw_rect.height) * 0.5)
        self.draw_surface.blit(image, draw_rect.topleft)
        
        if self.mode == 'view':
            self.draw_profile_info(self.draw_surface, (draw_rect.left + 50, draw_rect.top + 50))
            
            self.x_offset = draw_rect.left + 50
            self.y_offset = draw_rect.top + draw_rect.height - 50
            
            super(ProfileMenu, self).draw_buttons(self.draw_surface)
            
            # draw the player's ship
            if 'ship' in self.profile:
                image = None
                for btn in self.ship_selector.button_list:
                    if btn.attrs['state'] == int(self.profile['ship']):
                        image = btn.attrs['image'].copy()
                if image:
                    image = pygame.transform.rotate(image, self.ticks % 360)
                    self.draw_surface.blit(image, (draw_rect.center[0] - image.get_rect().center[0], draw_rect.center[1] - image.get_rect().center[1]))
            
            
        elif self.mode == 'select' or self.mode == 'edit' or self.mode == 'new' or self.mode == 'delete':
            super(ProfileMenu, self).draw_buttons(self.draw_surface)
            
        elif self.mode == 'ship-select':
            self.ship_selector.draw_buttons(self.draw_surface)
            
        
    def draw_profile_info(self, draw_surface, position):
        y = position[1]
        text = []
        text.append(('large', "Callsign: %s" % self.profile['name']))
        if 'shots-fired' in self.profile and float(self.profile['shots-fired']) > 0:
            accuracy = float(self.profile['shots-hit']) / float(self.profile['shots-fired']) * 100
        else:
            accuracy = 0.0
        text.append(('medium', "Stats:"))
        if not 'shots-fired' in self.profile:
            self.profile['shots-fired'] = 0
        if not 'shots-hit' in self.profile:
            self.profile['shots-hit'] = 0
        if not 'kills' in self.profile:
            self.profile['kills'] = 0
        if not 'deaths' in self.profile:
            self.profile['deaths'] = 0
        text.append(('small', "Shots fired: %i" % int(self.profile['shots-fired'])))
        text.append(('small', "Shots hit: %i" % int(self.profile['shots-hit'])))
        text.append(('small', "Accuracy: " + str(int(accuracy)) + "." + str(int((accuracy - int(accuracy)) * 10)) + "%"))
        text.append(('small', "Kills: %i" % int(self.profile['kills'])))
        text.append(('small', "Deaths: %i" % int(self.profile['deaths'])))
        if int(self.profile['deaths']) > 0:
            ratio = float(self.profile['kills']) / float(self.profile['deaths'])
        else:
            ratio = float(self.profile['kills'])
        text.append(('small', "Ratio: " + str(int(ratio)) + "." + str(int((ratio - int(ratio)) * 10))))
        
        for t in text:
            s = self.fonts[t[0]].render(t[1], 1, self.unselected_color)
            self.draw_surface.blit(s, (position[0], y))
            y += self.fonts[t[0]].size(t[1])[1] + 2
        
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
                                    ('Profile', MENU_PROFILE, None),
                                    ('Exit', MENU_EXIT, None)]))
        
        # menu 1 = options menu
        self.menuList.append(Menu(50, 50, 20, 5, 'vertical', 100, screen, None))
        menu = self.menuList[len(self.menuList) - 1]
        menu.add_button(TextInput('Width',self.parent.currentProfile['width'], MENU_OPTIONS, menu.font, menu.selected_color, menu.unselected_color, True, (self.parent.currentProfile, 'width')))
        menu.add_button(TextInput('Height',self.parent.currentProfile['height'], MENU_OPTIONS, menu.font, menu.selected_color, menu.unselected_color, True, (self.parent.currentProfile, 'height')))
        menu.add_button(SaveButton(menu, 'Apply', MENU_OPTIONS, None, menu.font, menu.selected_color, menu.unselected_color, self.parent.saveProfiles))
        menu.add_button(('Back', MENU_MAIN, None))
        
        # menu 2 = pause menu
        self.menuList.append(Menu(50, 50, 20, 5, 'vertical', 100, screen,
                                [('Resume', MENU_RESUME, None),
                                 ('Options', MENU_OPTIONS, None),
                                 ('Exit', MENU_EXIT, None)]))
        
        # menu 3 = mission menu
        menu = PagedMenu(50, 50, 50, 50, 4, screen, [])
        self.menuList.append(menu)
        for mission in self.parent.missionList:
            menu.add_button(MissionButton(self.parent, '', mission, mission[1], menu.font, menu.selected_color, menu.unselected_color))
        
        # ship selector menu
        menu = PagedMenu(50, 50, 50, 50, 4, screen, [])
        self.menuList.append(menu)
        for ship in self.parent.shipList:
            if ship.player_flyable:
                image, rect = Utils.load_image(ship.file, -1)
                image = pygame.transform.rotate(image, 90)
                menu.add_button(ShipButton(self.parent, '', MENU_OPTIONS, ship, image, menu.font, menu.selected_color, menu.unselected_color))
                if 'ship' in self.parent.currentProfile and int(self.parent.currentProfile['ship']) == ship.id:
                    menu.selected_btn = menu.button_list[len(menu.button_list) - 1]
                    
        menu = ProfileMenu(self.parent)
        self.menuList.append(menu)
                
    def draw(self):
        self.menuList[self.selectedMenu].redraw_all()
        self.menuList[self.selectedMenu].draw_buttons()
    
    def update(self, event = None):
        state = self.menuList[self.selectedMenu].update(event, self.selectedMenu)    
        if state != self.selectedMenu: self.menu_state_parse(state)
        
    
    def menu_state_parse(self, state = 0):
        if(state == MENU_MAIN):
            self.selectedMenu = MENU_MAIN
            if self.parent.gameState == self.parent.GAMESTATE_PAUSED:
                self.selectedMenu = MENU_PAUSE
        elif(state == MENU_RESUME):
            self.selectedMenu = -1
        elif(state == MENU_EXIT):
            sys.exit(0)
        elif state == -1:
            pass
        else:
            self.selectedMenu = state

        self.menuList[self.selectedMenu].update(
                            pygame.event.Event(EVENT_CHANGE_STATE, key = 0),
                            self.selectedMenu)
        return self.selectedMenu
    
    def is_active(self):
        if self.selectedMenu >= 0 and self.selectedMenu < len(self.menuList):
            return True
        else:
            return False