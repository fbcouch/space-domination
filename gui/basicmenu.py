'''
Created on Aug 16, 2012

@author: Jami
'''
from gui import Element, Frame
from pygame.locals import *
import Utils
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
                #self.active = False
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
        
class PagedMenu(Frame):
    
    items = None # list of tuples (image, value)
    page = 1
    num_per_page = 4
    
    next_btn = None
    prev_btn = None
    page_indicator = None
    back_btn = None

    h_pad = 0
    v_pad = 0
    
    selected_item = None
    
    font = None
    
    item_callback = None
    back_btn_callback = None
    back_btn_text = ""
    
    def __init__(self, parent, **kwargs):
        super(PagedMenu, self).__init__(parent, **kwargs)
        
        self.num_per_page = int(kwargs.get('per_page', 4))
        self.h_pad = int(kwargs.get('h_pad', 50))
        self.v_pad = int(kwargs.get('v_pad', 10))
        self.items = kwargs.get('items', [])
        self.item_callback = kwargs.get('item_callback', None)
        self.build_from_list()
        
        self.font = kwargs.get('font', pygame.font.Font(None, 24))
        
        arrows = Utils.load_sprite_sheet('arrows.png', 69, 100, -1)
        arrows_rev = []
        for arrow in arrows:
            image = arrow.copy()
            image = pygame.transform.flip(image, True, False)
            arrows_rev.append(image)
        
        self.next_btn = TogglableImageButton(self, arrows, callback = self.next_page_click)
        self.prev_btn = TogglableImageButton(self, arrows_rev, callback = self.prev_page_click)
        
        self.back_btn_callback = kwargs.get('back_btn_callback', None)
        self.back_text = kwargs.get('back_btn_text', 'Back')
        
        
        self.back_btn = BasicTextButton(self, text = self.back_text, callback = self.back_btn_callback, font = self.font)
        
    def build_from_list(self, items = None):
        '''build the menu using a list of items...'''
        if items:
            self.items = items
        
        n = 0
        for item in self.items:
            # add a button to the child list for each item
            n += 1
            self.add_child(BasicImageButton(self, image = item[0], select_fxn = self.mouse_over_callback, unselect_fxn = self.mouse_off_callback, callback = self.item_callback, callback_kwargs = {'value': item[1]}))
    
    def update(self, event):
        #super(MissionMenu, self).update(event)
        num_pages = self.get_num_pages()
        
        if self.page < 1: self.page = 1
        if self.page > num_pages: self.page = num_pages
        
        start_i = (self.page - 1) * self.num_per_page
        end_i = self.page * self.num_per_page
        if end_i > len(self.items): end_i = len(self.items)
        
        for i in range(start_i, end_i):
            self.children[i].update(event)
        
        if len(self.children) > len(self.items):
            for i in range(len(self.items), len(self.children)):
                self.children[i].update(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back_btn_callback()
                return True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                item = self.get_next_btn(self.selected_item)
                if self.selected_item: self.selected_item.on_mouse_off()
                item.on_mouse_over()
                self.selected_item = item
                
                return True
            elif event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                item = self.get_prev_btn(self.selected_item)
                if self.selected_item: self.selected_item.on_mouse_off()
                item.on_mouse_over()
                self.selected_item = item
                return True
            elif event.key == pygame.K_RETURN:
                if self.selected_item:
                    self.selected_item.on_click()
                    return True
        return False
    
    def get_num_pages(self):
        num_pages = len(self.items) / float(self.num_per_page)
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
        if end_i > len(self.items): end_i = len(self.items)
        
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
        
        if self.prev_btn.rect.left < draw_rect.left:
            draw_rect.left = self.prev_btn.rect.left
            
        if self.prev_btn.rect.top < draw_rect.top:
            draw_rect.top = self.prev_btn.rect.top
            
        if self.next_btn.rect.left + self.next_btn.rect.width > draw_rect.left + draw_rect.width:
            draw_rect.width = self.next_btn.rect.left + self.next_btn.rect.width - draw_rect.left
            
        if self.next_btn.rect.top + self.next_btn.rect.height > draw_rect.top + draw_rect.height:
            draw_rect.height = self.next_btn.rect.top + self.next_btn.rect.height - draw_rect.top
        
        # draw the back to main menu button
        x = draw_rect.left
        y = draw_rect.top - self.v_pad * 3 - self.back_btn.rect.height
        self.back_btn.rect.topleft = (x, y)
        self.back_btn.draw()
        
        draw_rect.height += draw_rect.top - y
        draw_rect.top = y
        
        
        return draw_rect
    
    
    
    def get_next_btn(self, current):
        if current is None:
            if len(self.children) > 0: return self.children[0]
            return None
        if current is self.next_btn:
            return self.back_btn
        elif current is self.back_btn and self.prev_btn.is_enabled():
            return self.prev_btn
        elif current is self.prev_btn or current is self.back_btn:
            # set to the first item displayed
            return self.children[(self.page - 1) * self.num_per_page]
        else:
            new_i = self.children.index(current) + 1
            
            if new_i >= self.page * self.num_per_page or new_i >= len(self.children) - 3:
                if self.next_btn.is_enabled():
                    return self.next_btn
                else:
                    return self.back_btn
                
            return self.children[new_i]
    
    def get_prev_btn(self, current):
        if current is None:
            if len(self.children) > 0: return self.children[0]
            return None
        if current is self.prev_btn:
            return self.back_btn
        elif current is self.back_btn and self.next_btn.is_enabled():
            return self.next_btn
        elif current is self.next_btn or current is self.back_btn:
            # set to the last item displayed
            i = self.page * self.num_per_page - 1
            if i >= len(self.children) - 4:
                i = len(self.children) - 4
                
            return self.children[i]
        else:
            new_i = self.children.index(current) - 1

            if new_i < (self.page - 1) * self.num_per_page:
                if self.prev_btn.is_enabled():
                    return self.prev_btn
                else:
                    return self.back_btn
            return self.children[new_i]
    
    def mouse_over_callback(self, child):
        pass
        
    def mouse_off_callback(self, child):
        pass
        
    def next_page_click(self, **kwargs):
        self.page += 1
    
    def prev_page_click(self, **kwargs):
        self.page -= 1
    
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

class ImageLabel(Element):
    
    rotate = None
    original = None
    
    angle = 0
    
    def __init__(self, parent, image, **kwargs):
        super(ImageLabel, self).__init__(parent, **kwargs)
        self.image = image
        self.rect = image.get_rect()
        self.rotate = bool(kwargs.get('rotate', False))
        self.angle = int(kwargs.get('angle', 0))
        self.original = self.image.copy()
        self.apply_rotate()
        
    def draw(self):
        super(ImageLabel, self).draw()
        if self.rotate:
            self.angle += 1
            self.apply_rotate()
        
    def apply_rotate(self):
        self.angle = self.angle % 360
        self.image = pygame.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        
    def get_image(self):
        return self.image

class DropdownSelector(Element):
    '''the dropdown selector will basically act as a Label that has some text and a little arrow at the end of it'''
    
    item_list = None # items should be a tuple (display_str, return_value)
    selected_item = None
    
    expanded = False
    
    arrow = None
    border_color = None
    font = None
    font_color = None
    
    v_pad = 0
    
    on_select = None
    
    def __init__(self, parent, items, selected = None, **kwargs):
        '''Constructor'''
        super(DropdownSelector, self).__init__(parent, **kwargs)
        
        self.item_list = items
        if selected and selected in self.item_list:
            self.selected_item = selected
        else:
            self.selected_item = self.item_list[0]
        
        self.set_item(self.selected_item)
        
        self.arrow = kwargs.get('arrow', Utils.load_image('gui_dropdown_arrow.png', -1)[0])
        self.border_color = kwargs.get('border_color', (200, 200, 200))
        self.font = kwargs.get('font', pygame.font.Font(None, 24))
        self.font_color = kwargs.get('font_color', (255, 255, 255))
        
        self.v_pad = kwargs.get('v_pad', 5)
        self.rect = pygame.rect.Rect(0,0,0,0)
        
        self.on_select = kwargs.get('on_select', None)
        
        self.collapse()
        
    def set_item(self, item):
        if item not in self.item_list:
            self.item_list.insert(0, item)
        else:
            self.item_list.remove(item)
            self.item_list.insert(0, item)
        self.selected_item = item
        
    def on_click(self, **kwargs):
        
        if self.expanded:
            
            y = self.rect.top
            pos = kwargs.get('pos', (-1, -1))
            for item in self.item_list:
                itemsize = self.font.size(item[0])
                itemrect = pygame.rect.Rect(self.rect.left, y, self.rect.width, itemsize[1] + self.v_pad)
                print str(itemrect) + ":" + str(pos) + "?" + str(itemrect.collidepoint(pos))
                if itemrect.collidepoint(pos):
                    self.set_item(item)
                    if self.on_select: self.on_select(value = item[1])
                    break
                y += itemsize[1] + self.v_pad
            self.collapse()
        else:
            self.expand()
        
    def collapse(self):
        self.expanded = False
        textsize = self.font.size(self.selected_item[0])
        w = 0
        for item in self.item_list:
            if self.font.size(item[0])[0] > w:
                w = self.font.size(item[0])[0]
        
        w += self.arrow.get_width()
        h = textsize[1]
        if self.arrow.get_height() > h:
            h = self.arrow.get_height()
        self.image = pygame.surface.Surface((w + 2, h + 2))
        self.image.blit(self.font.render(self.selected_item[0], 1, self.font_color), (1,1))
        self.image.blit(self.arrow, (self.image.get_width() - self.arrow.get_width() - 1, h - self.arrow.get_height()))
        pygame.gfxdraw.rectangle(self.image, self.image.get_rect(), self.border_color)
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        
    def expand(self):
        self.expanded = True
        w = 0
        h = 0
        for item in self.item_list:
            item_size = self.font.size(item[0])
            if item_size[0] > w:
                w = item_size[0]
            h += item_size[1] + self.v_pad
                
        self.image = pygame.surface.Surface((w + self.arrow.get_width() + 2, h + 2))
        
        y = 0
        for item in self.item_list:
            self.image.blit(self.font.render(item[0], 1, self.font_color), (1, y + 1))
            
            y += self.font.size(item[0])[1] + self.v_pad
        
        uparrow = pygame.transform.flip(self.arrow, False, True)
        self.image.blit(uparrow, (self.image.get_width() - uparrow.get_width() - 1, 1))
        pygame.gfxdraw.rectangle(self.image, self.image.get_rect(), self.border_color)
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        
    def draw(self):
        super(DropdownSelector, self).draw()

class BasicCheckbox(BasicImageButton):
    text = ""
    checked = None
    unchecked = None
    value = False
    
    def __init__(self, parent, **kwargs):
        super(BasicImageButton, self).__init__(parent, **kwargs)
        self.text = kwargs.get('text', "Checkbox")
        self.font = kwargs.get('font', pygame.font.Font(None, 32))
        self.value = kwargs.get('value', False)
        
        self.checked = pygame.surface.Surface((22,22))
        self.checked.set_colorkey(self.checked.get_at((0,0)))
        pygame.gfxdraw.rectangle(self.checked, self.checked.get_rect(), (255, 255, 255))
        self.unchecked = self.checked.copy()
        self.checked.blit(self.font.render("X", 1, (255, 255, 255)), ((self.checked.get_width() - self.font.size("X")[0]) * 0.5 , (self.checked.get_height() - self.font.size("Y")[1]) * 0.5))
        
        self.create_images()
        
        self.callback = kwargs.get('callback', None)
        self.callback_kwargs = kwargs.get('callback_kwargs', {})
        self.select_fxn = kwargs.get('select_fxn', None)
        self.unselect_fxn = kwargs.get('unselect_fxn', None)
        
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect()
        
    def create_images(self):
        size = self.font.size(self.text)
        image = pygame.surface.Surface((size[0] + self.checked.get_width() + 8, size[1]))
        
        self.unselected_image = image.copy()
        self.selected_image = image.copy() 
        self.unselected_image.blit(self.font.render(self.text, 1, (255, 255, 255)), (0,0))
        self.selected_image.blit(self.font.render(self.text, 1, (255, 0, 0)), (0,0))
        if self.value:
            self.unselected_image.blit(self.checked, (size[0] + 8, 0))
            self.selected_image.blit(self.checked, (size[0] + 8, 0))
        else:
            self.unselected_image.blit(self.unchecked, (size[0] + 8, 0))
            self.selected_image.blit(self.unchecked, (size[0] + 8, 0))
            
    def on_click(self, **kwargs):
        if self.value:
            self.value = False
        else:
            self.value = True
        self.create_images()

        