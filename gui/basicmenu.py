'''
Created on Aug 16, 2012

@author: Jami
'''
from gui import Frame
import pygame

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
        pass
    
    def draw(self):
        # TODO implement drawing function
        pass
    