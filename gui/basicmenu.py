'''
Created on Aug 16, 2012

@author: Jami
'''
from gui import Element, Frame
from pygame.locals import *
import pygame
import sys
import traceback

DEFAULT_SELECTED_COLOR = (255, 0, 0)
DEFAULT_UNSELECTED_COLOR = (255, 255, 255)

class BasicMenu(Frame):
    '''
    This is a basic menu that will display with given attributes on the screen.
    '''
    x_offset = 0
    y_offset = 0
    h_pad = 0
    v_pad = 0
    orientation = 'vertical'
    num_per_rowcol = 0
    
    font = None
    
    centered_on_screen = True
    h_align = 'center'
    v_align = 'center'
    
    selected_color = None
    unselected_color = None
    
    selected_btn = None
    
    on_close = None

    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        super(BasicMenu, self).__init__(parent, **kwargs)
        
        self.x_offset = kwargs.get('x_offset', 0)
        self.y_offset = kwargs.get('y_offset', 0)
        self.h_pad = kwargs.get('h_pad', 0)
        self.v_pad = kwargs.get('v_pad', 0)
        self.orientation = kwargs.get('orientation', 'vertical')
        self.num_per_rowcol = kwargs.get('num', 5)
        self.font = kwargs.get('font', None)
        if not self.font:
            self.font = pygame.font.Font(None, 20)
        self.centered_on_screen = kwargs.get('centered', True)
        self.h_align = kwargs.get('h_align', 'center')
        self.v_align = kwargs.get('v_align', 'center')
        self.selected_color = kwargs.get('selected_color', DEFAULT_SELECTED_COLOR)
        self.unselected_color = kwargs.get('unselected_color', DEFAULT_UNSELECTED_COLOR)
        self.on_close = kwargs.get('on_close', None)
        
    def add_child(self, child):
        super(BasicMenu, self).add_child(child)
        if not self.selected_btn:
            self.selected_btn = child
    
    def update(self, event):
        return_val = False
        
        if self.selected_btn is None and len(self.children) > 0:
            self.selected_btn = self.children[0]
        
        if not len(self.children) > 0:
            return False
        
        # handle key events
        if event.type == pygame.KEYDOWN:
            sel_item = self.children.index(self.selected_btn)
            
            if self.orientation == 'vertical':
                if event.key == pygame.K_UP:
                    if sel_item > 0:
                        sel_item -= 1
                    else:
                        sel_item = len(self.children) - 1
                elif event.key == pygame.K_DOWN:
                    if sel_item < len(self.children) - 1:
                        sel_item += 1
                    else:
                        sel_item = 0
            elif self.orientation == 'horizontal':
                if event.key == pygame.K_LEFT:
                    if sel_item > 0:
                        sel_item -= 1
                    else:
                        sel_item = len(self.children) - 1
                elif event.key == pygame.K_RIGHT:
                    if sel_item < len(self.children) - 1:
                        sel_item += 1
                    else:
                        sel_item = 0
            if event.key == pygame.K_RETURN:
                if self.selected_btn:
                    return self.selected_btn.on_click()
                
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                if self.on_close:
                    self.on_close()
            
            self.selected_btn.on_mouse_off()
            self.selected_btn = self.children[sel_item]
            if not ((self.orientation == 'vertical' and (event.key == pygame.K_UP or event.key == pygame.K_DOWN)) and (self.orientation == 'horizontal' and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT))):
                return_val = self.selected_btn.update(event)
                
            else:
                return_val = True
            self.selected_btn.on_mouse_over()
            return return_val
        else:
            # handle other events
            return_val = super(BasicMenu, self).update(event)
            
        
        if self.selected_btn:
            self.selected_btn.on_mouse_over()
        return return_val
    
    def draw(self):
        draw_surface = pygame.display.get_surface()
        
        bounding_rect, col_widths, row_heights = self.get_draw_rect()
        
        row = 0
        col = 0
        
        if self.centered_on_screen:
            x = (draw_surface.get_width() - bounding_rect.width) * 0.5
            y = (draw_surface.get_height() - bounding_rect.height) * 0.5
        else:
            x = self.x_offset
            y = self.y_offset
        bounding_rect.left = x
        bounding_rect.top = y
        x_start = x
        y_start = y
        for button in self.children:
            if self.orientation == 'vertical':
                if row >= self.num_per_rowcol:
                    row = 0
                    x += col_widths[col] + self.h_pad
                    col += 1
                    y = y_start
                
                #button.draw(draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                draw_x = x
                if self.h_align == 'left':
                    draw_x = x
                elif self.h_align == 'center':
                    draw_x += (col_widths[col] - button.rect.width) * 0.5
                elif self.h_align == 'right':
                    draw_x += col_widths[col] - button.rect.width
                    
                draw_y = y
                if self.v_align == 'top':
                    draw_y = y
                elif self.v_align == 'center':
                    draw_y += (row_heights[row] - button.rect.height) * 0.5
                elif self.v_align == 'bottom':
                    draw_y += row_heights[row] - button.rect.height
                button.rect.topleft = (draw_x, draw_y)
                button.draw()
                y += row_heights[row] + self.v_pad
                row += 1
            
            else:
                if col >= self.num_per_rowcol:
                    col = 0
                    y += row_heights[row] + self.v_pad
                    row += 1
                    x = x_start
                
                #button.draw(self.draw_surface, x, y, col_widths[col], row_heights[row], self.centered, button is self.selected_btn)
                draw_x = x
                if self.h_align == 'left':
                    draw_x = x
                elif self.h_align == 'center':
                    draw_x += (col_widths[col] - button.rect.width) * 0.5
                elif self.h_align == 'right':
                    draw_x += col_widths[col] - button.rect.width
                    
                draw_y = y
                if self.v_align == 'top':
                    draw_y = y
                elif self.v_align == 'center':
                    draw_y += (row_heights[row] - button.rect.height) * 0.5
                elif self.v_align == 'bottom':
                    draw_y += row_heights[row] - button.rect.height
                button.rect.topleft = (draw_x, draw_y)
                button.draw()
                
                x += col_widths[col] + self.h_pad
                col += 1
        
    def get_draw_rect(self):
        '''returns a rectangle which will contain all the children, the col widths, and the row heights'''
        # TODO clean this up
        bounding_rect = pygame.rect.Rect(0,0,0,0)
        
        y = 0
        x = 0
        row = 0
        col = 0
        col_widths = []
        row_heights = []
        for button in self.children:
            if self.orientation == 'vertical':
                if row >= self.num_per_rowcol:
                    row = 0
                    x += col_widths[col] + self.h_pad
                    col += 1
                    col_widths.append(0)
                    y = 0

                y += button.rect.height
                if row > 0: y += self.v_pad
                
                if col >= len(col_widths):
                    col_widths.append(button.rect.width)
                elif button.rect.width > col_widths[col]:
                    col_widths[col] = button.rect.width
                
                if col == 0:
                    row_heights.append(button.rect.height)
                elif button.rect.height > row_heights[row]:
                    row_heights[row] = button.rect.height
                row += 1
            
            else:
                if col >= self.num_per_rowcol:
                    col = 0
                    y += row_heights[row] + self.v_pad
                    row += 1
                    row_heights.append(0)
                    x = 0
                
                x += button.rect.width
                if col > 0: x += self.h_pad
                
                
                if row >= len(row_heights):
                    row_heights.append(button.rect.height)
                elif button.rect.height > row_heights[row]:
                    row_heights[row] = button.rect.height
                
                if row == 0:
                    col_widths.append(button.rect.width)
                elif button.rect.width > col_widths[col]:
                    col_widths[col] = button.rect.width
                
                col += 1
            
            
        if col < len(col_widths) and self.orientation == 'vertical':
            x += col_widths[col]
        elif row < len(row_heights):
            y += row_heights[row]
        
        x = -1 * self.h_pad
        for c in col_widths:
            x += c + self.h_pad
        bounding_rect.width = x
        y = -1 * self.v_pad
        for r in row_heights:
            y += r + self.v_pad
        bounding_rect.height = y
        
        return bounding_rect, col_widths, row_heights

    def mouse_over_callback(self, child):
        '''this allows mouse movement to change the selection as the keyboard does'''
        if self.selected_btn and child is not self.selected_btn:
            self.selected_btn.on_mouse_off()
        self.selected_btn = child
        
    
    
class BasicTextButton(Element):
    
    text = ""
    selected_image = None
    unselected_image = None
    font = None
    callback = None
    callback_kwargs = None
    select_fxn = None
    
    def __init__(self, parent, **kwargs):
        super(BasicTextButton, self).__init__(parent, **kwargs)
        self.text = kwargs.get('text', 'default button')
        self.font = kwargs.get('font', None)
        self.callback = kwargs.get('callback', None)
        self.select_fxn = kwargs.get('select_fxn', None)
        self.callback_kwargs = kwargs.get('callback_kwargs', None)
        if not self.font:
            self.font = pygame.font.Font(None, 32)
            
        self.selected_image = self.font.render(self.text, 1, kwargs.get('selected_color', DEFAULT_SELECTED_COLOR))
        self.unselected_image = self.font.render(self.text, 1, kwargs.get('unselected_color', DEFAULT_UNSELECTED_COLOR))
        
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect()
        
    def on_click(self, **kwargs):
        if self.callback:
            if self.callback_kwargs:
                return self.callback(**self.callback_kwargs)
            else:
                return self.callback()
    
    def on_mouse_over(self):
        self.image = self.selected_image.copy()
        self.rect = self.image.get_rect(center = self.rect.center)
        if self.select_fxn:
            self.select_fxn(self)
    
    def on_mouse_off(self):
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect(center = self.rect.center)

class BasicImageButton(Element):
    
    image = None
    selected_image = None
    unselected_image = None
    callback = None
    callback_kwargs = None
    select_fxn = None
    unselect_fxn = None
    
    def __init__(self, parent, **kwargs):
        super(BasicImageButton, self).__init__(parent, **kwargs)
        self.font = kwargs.get('font', None)
        if not self.font:
            self.font = pygame.font.Font(None, 32)
        image = kwargs.get('image', self.font.render("image button", 1, DEFAULT_UNSELECTED_COLOR))
        self.callback = kwargs.get('callback', None)
        self.callback_kwargs = kwargs.get('callback_kwargs', None)
        self.select_fxn = kwargs.get('select_fxn', None)
        self.unselect_fxn = kwargs.get('unselect_fxn', None)
        
        self.unselected_image = kwargs.get('unselected_image', image.copy())
        self.selected_image = kwargs.get('selected_image', self.generate_selected_image(self.unselected_image))
        
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect()
        
    def generate_selected_image(self, image):
        '''create a 'selected image' from image'''
        
        temp_image = pygame.surface.Surface((image.get_width() + 4, image.get_height() + 4))
        temp_image = temp_image.convert()
        temp_image.blit(image, (2,2))
        temp_image.set_colorkey(temp_image.get_at((0,0)))
        pygame.gfxdraw.rectangle(temp_image, pygame.rect.Rect(0,0,temp_image.get_width(), temp_image.get_height()), DEFAULT_SELECTED_COLOR)
        pygame.gfxdraw.rectangle(temp_image, pygame.rect.Rect(1,1,temp_image.get_width()-2, temp_image.get_height()-2), DEFAULT_SELECTED_COLOR)
        
        return temp_image
        
    def on_click(self, **kwargs):
        if self.callback:
            if self.callback_kwargs:
                return self.callback(**self.callback_kwargs)
            else:
                return self.callback()
    
    def on_mouse_over(self):
        self.image = self.selected_image.copy()
        #self.rect = self.image.get_rect()
        if self.select_fxn:
            self.select_fxn(self)
    
    def on_mouse_off(self):
        self.image = self.unselected_image.copy()
        if self.unselect_fxn:
            self.unselect_fxn(self)
        #self.rect = self.image.get_rect()

class TogglableImageButton(Element):
    
    disabled_image = None
    unselected_image = None
    selected_image = None
    
    enabled = False
    
    callback = None
    callback_kwargs = None
    
    def __init__(self, parent, sprite_sheet, **kwargs):
        super(TogglableImageButton, self).__init__(parent, **kwargs)
        
        self.disabled_image = sprite_sheet[0]
        self.unselected_image = sprite_sheet[1]
        self.selected_image = sprite_sheet[2]
        
        self.set_enabled(kwargs.get('enabled', False))
        self.callback = kwargs.get('callback', None)
        self.callback_kwargs = kwargs.get('callback_kwargs', None)
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        if self.enabled:
            self.image = self.unselected_image
        else:
            self.image = self.disabled_image
        self.rect = self.image.get_rect()
    
    def is_enabled(self):
        return self.enabled
    
    def on_click(self, **kwargs):
        if not self.is_enabled(): return
        if self.callback_kwargs:
            return self.callback(**self.callback_kwargs)
        else:
            return self.callback()
        
    def on_mouse_over(self):
        if self.enabled:
            self.image = self.selected_image
        else:
            self.image = self.disabled_image
        self.rect = self.image.get_rect()
            
    def on_mouse_off(self):
        if self.enabled:
            self.image = self.unselected_image
        else:
            self.image = self.disabled_image
        self.rect = self.image.get_rect()

class BasicTextInput(Element):
    
    label = ''
    value = ''
    selected_color = None
    unselected_color = None
    
    font = None
    callback = None
    callback_kwargs = None
    select_fxn = None
    
    numbers_only = False
    
    keymap = {K_0: '0', K_1: '1', K_2: '2', K_3: '3', K_4: '4', K_5: '5', K_6: '6', K_7: '7', K_8: '8', K_9: '9',
              K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e', K_f: 'f', K_g: 'g', K_h: 'h', K_i: 'i', K_j: 'j', 
              K_k: 'k', K_l: 'l', K_m: 'm', K_n: 'n', K_o: 'o', K_p: 'p', K_q: 'q', K_r: 'r', K_s: 's', K_t: 't', 
              K_u: 'u', K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y', K_z: 'z', K_MINUS: '-', K_UNDERSCORE: '_'}
    numbers = {K_0: '0', K_1: '1', K_2: '2', K_3: '3', K_4: '4', K_5: '5', K_6: '6', K_7: '7', K_8: '8', K_9: '9'}
    
    
    def __init__(self, parent, **kwargs):
        super(BasicTextInput, self).__init__(parent, **kwargs)
        
        self.label = kwargs.get('label', '')
        self.value = kwargs.get('value', '')
        self.selected_color = kwargs.get('selected_color', DEFAULT_SELECTED_COLOR)
        self.unselected_color = kwargs.get('unselected_color', DEFAULT_UNSELECTED_COLOR)
        self.font = kwargs.get('font', pygame.font.Font(None, 32))
        self.callback = kwargs.get('callback', None)
        self.callback_kwargs = kwargs.get('callback_kwargs', None)
        self.select_fxn = kwargs.get('select_fxn', None)
        self.numbers_only = bool(kwargs.get('numbers_only', False))
        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        
        self.set_unselected_image()
        
    def set_unselected_image(self):
        self.image = self.font.render("%s: %s" % (self.label, str(self.value)), 1, self.unselected_color)
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        
    def set_selected_image(self):
        self.image = self.font.render("%s: %s_" % (self.label, str(self.value)), 1, self.selected_color)
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        
    def on_mouse_over(self):
        self.set_selected_image()
        if self.select_fxn:
            self.select_fxn(self)
        
    def on_mouse_off(self):
        self.set_unselected_image()
        if self.select_fxn:
            self.select_fxn(self)
        
    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if (self.numbers_only and event.key in self.numbers) or (not self.numbers_only and event.key in self.keymap):
                # valid keystroke
                self.value = str(self.value) + self.keymap[event.key]
                self.set_selected_image()
                return True # event was handled
            elif event.key == pygame.K_BACKSPACE:
                if len(str(self.value)) > 0:
                    self.value = str(self.value)[:len(str(self.value)) - 1]
                    self.set_selected_image()
                return True # event was handled
        return super(BasicTextInput, self).update(event)
    
    
    