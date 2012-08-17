'''
Created on Aug 16, 2012

@author: Jami
'''
from gui import Element, Frame
import pygame
import sys

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
        
    def update(self, events):
        # TODO implement an updating function
        if self.selected_btn is None and len(self.children) > 0:
            self.selected_btn = self.children[0]
        
        if not len(self.children) > 0:
            return
        
        # handle key events
        for event in events:
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
                    self.selected_btn.on_click()
                    
                elif event.key == pygame.K_ESCAPE:
                    self.active = False
                    # TODO callback to the parent here?
                self.selected_btn.on_mouse_off()
                self.selected_btn = self.children[sel_item]
        super(BasicMenu, self).update(events)
        
        if self.selected_btn:
            self.selected_btn.on_mouse_over()
    
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
                button.rect.topleft = (x, y)
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
                button.rect.topleft = (x, y)
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
        if child is not self.selected_btn:
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
            self.font = pygame.font.Font(None, 20)
            
        self.selected_image = self.font.render(self.text, 1, kwargs.get('selected_color', DEFAULT_SELECTED_COLOR))
        self.unselected_image = self.font.render(self.text, 1, kwargs.get('unselected_color', DEFAULT_UNSELECTED_COLOR))
        
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect()
        
    def on_click(self):
        if self.callback:
            if self.callback_kwargs:
                return self.callback(**self.callback_kwargs)
            else:
                return self.callback()
    
    def on_mouse_over(self):
        self.image = self.selected_image.copy()
        self.rect = self.image.get_rect()
        if self.select_fxn:
            self.select_fxn(self)
    
    def on_mouse_off(self):
        self.image = self.unselected_image.copy()
        self.rect = self.image.get_rect()
        