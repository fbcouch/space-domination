'''
Created on Aug 16, 2012

@author: Jami
'''
import pygame
import sys

class Frame(object):
    '''abstract class from which frames may be implemented'''
    
    parent = None
    children = None
    active = False
    
    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        
        self.parent = parent
        self.children = []
    
    def update(self, events):
        for child in self.children:
            if child.is_active(): child.update(events)
    
    def draw(self):
        for child in self.children:
            if child.is_active(): child.draw()
    
    def is_active(self):
        return self.active
    
    def set_active(self, active):
        self.active = active
        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self

class GUI(Frame):
    '''
    the main manager class and entry point for using the GUI
    '''
    parent = None
    children = None
    active = False
    
    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        self.parent = parent
        self.children = []
    
    def update(self, events):
        for child in self.children:
            if child.is_active(): child.update(events)
    
    def draw(self):
        for child in self.children:
            if child.is_active(): child.draw()
            
class Element(pygame.sprite.Sprite):
    '''abstract class from which gui elements can be constructed'''
    
    parent = None
    active = True
    
    mouse_btn_down = None
    mouse_over = False
    
    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        self.parent = parent
        if self.parent and not self in self.parent.children:
            self.parent.add_child(self)
        self.mouse_btn_down = {}
    
    def update(self, events):
        # TODO implement dragging
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                print "MOUSEMOTION pos (%s), rel (%s), buttons (%s)" % (event.pos, event.rel, event.buttons)
                if not self.mouse_over and self.rect.collidepoint(event.pos):
                    # mouse is freshly over the element
                    self.on_mouse_over()
                    self.mouse_over = True
                elif self.mouse_over and not self.rect.collidepoint(event.pos):
                    # mouse was on and is leaving the element
                    self.on_mouse_off()
                    self.mouse_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # record where the button was pressed and call on mouse btn down
                    self.set_mouse_btn(event.button, event.pos)
                    self.on_mouse_btn_down(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.on_mouse_btn_up(event.button)
                    if self.get_mouse_btn(event.button):
                        # make sure the button was pressed down on this element
                        self.on_click()
                    self.set_mouse_btn(event.button, False)
                        
                        
    
    def set_mouse_btn(self, btn, status):
        self.mouse_btn_down[btn] = status
        
    def get_mouse_btn(self, btn):
        if btn in self.mouse_btn_down:
            return self.mouse_btn_down[btn]
        else:
            return False
    
    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
    
    def on_click(self):
        pass
    
    def on_mouse_over(self):
        pass
    
    def on_mouse_off(self):
        pass
    
    def on_mouse_btn_down(self, button):
        pass
    
    def on_mouse_btn_up(self, button):
        pass
    
    def on_drag(self):
        pass
    
    def on_drop(self):
        pass
    
    def on_drop_target(self, element):
        pass
    
    def is_active(self):
        return True
    
class TestElement(Element):
    def on_mouse_over(self):
        self.image.fill((255, 0, 0))
    
    def on_mouse_off(self):
        self.image.fill((51, 102, 255))
    
    def on_mouse_btn_down(self, button):
        self.image.fill((0, 255, 0))
    
    def on_mouse_btn_up(self, button):
        self.image.fill((51, 102, 255))
        
    def on_click(self):
        self.image.fill((255, 255, 255))
    
if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Testing GUI")
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    font = None
    if pygame.font:
        font = pygame.font.Font(None, 20)
    
    gui = GUI(None)
    gui.set_active(True)
    
    frame = Frame(gui)
    gui.add_child(frame)
    frame.set_active(True)
    
    testel = TestElement(frame)
    testel.image = pygame.surface.Surface((100,50))
    testel.image = testel.image.convert()
    testel.image.fill((51, 102, 255))
    testel.rect = testel.image.get_rect()
    testel.rect.topleft = ((window.get_width() - testel.rect.width) * 0.5, (window.get_height() - testel.rect.height) * 0.5)
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
        
        if gui.is_active(): gui.update(events)
        
        screen.blit(background, (0,0))
        
        if gui.is_active(): gui.draw()
        
        pygame.display.flip()
        