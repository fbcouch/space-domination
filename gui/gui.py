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
    
    def update(self, event):
        for child in self.children:
            if child.is_active(): child.update(event)
    
    def draw(self):
        for child in self.children:
            if child.is_active(): child.draw()
    
    def is_active(self):
        return self.active
    
    def set_active(self, active):
        self.active = active
        
    def add_child(self, child):
        if not child in self.children:
            self.children.append(child)
        child.parent = self

class GUI(Frame):
    '''
    the main manager class and entry point for using the GUI
    '''
    parent = None
    children = None
    active = False
    
    main_menu = None
    options_menu = None
    profile_menu = None
    mission_menu = None
    pause_menu = None
    
    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        self.parent = parent
        self.children = []
    
    def update(self, event):
        for child in self.children:
            if child.is_active(): child.update(event)
    
    def draw(self):
        for child in self.children:
            if child.is_active(): child.draw()
    
    '''some basic functionality'''        
    def exit_click(self):
        '''exit the game'''
        sys.exit(0)
    
    def main_menu_click(self):
        '''open the main menu'''
        if self.main_menu in self.children:
            self.generic_click(target_id = self.children.index(self.main_menu)) 
        '''for child in self.children:
            if child is self.main_menu:
                child.set_active(True)
                self.set_active(True)
            else:
                child.set_active(False)'''
        
        
    def options_menu_click(self):
        '''open the options menu'''
        pass
    
    def profile_menu_click(self):
        '''open the profile menu'''
        pass
    
    def mission_menu_click(self):
        '''open the mission menu'''
        if self.mission_menu in self.children:
            self.generic_click(target_id = self.children.index(self.mission_menu))
    
    def pause_menu_click(self):
        if self.pause_menu in self.children:
            self.generic_click(target_id = self.children.index(self.pause_menu)) 
    
    def generic_click(self, **kwargs):
        '''generic click with args passed'''
        if 'target_id' in kwargs:
            id = int(kwargs.get('target_id', -1))
            if id >= 0 and id < len(self.children):
                # ID is in the proper range to call up a child
                for child in self.children:
                    if self.children.index(child) == id:
                        child.set_active(True)
                    else:
                        child.set_active(False)
            self.set_active(True)
            
    def close(self):
        for child in self.children:
            child.set_active(False)
        self.set_active(False)
        
    
            
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
    
    def update(self, event):
        # TODO implement dragging
        if event.type == pygame.MOUSEMOTION:
            #print "MOUSEMOTION pos (%s), rel (%s), buttons (%s)" % (event.pos, event.rel, event.buttons)
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
    
