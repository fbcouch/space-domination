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
            if child.is_active(): 
                if child.update(event):
                    return True
        return False
    
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
            if child.is_active(): 
                if child.update(event):
                    return True
    
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
            return self.generic_click(target_id = self.children.index(self.main_menu))
        return False
        '''for child in self.children:
            if child is self.main_menu:
                child.set_active(True)
                self.set_active(True)
            else:
                child.set_active(False)'''
        
        
    def options_menu_click(self):
        '''open the options menu'''
        if self.options_menu in self.children:
            return self.generic_click(target_id = self.children.index(self.options_menu))
        return False
    
    def profile_menu_click(self):
        '''open the profile menu'''
        if self.profile_menu in self.children:
            return self.generic_click(target_id = self.children.index(self.profile_menu))
        return False
    
    def mission_menu_click(self):
        '''open the mission menu'''
        if self.mission_menu in self.children:
            return self.generic_click(target_id = self.children.index(self.mission_menu))
        return False
    
    def pause_menu_click(self):
        if self.pause_menu in self.children:
            return self.generic_click(target_id = self.children.index(self.pause_menu)) 
        return False
    
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
            return True
            
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
                returnval = self.on_mouse_over()
                self.mouse_over = True
                return returnval
            elif self.mouse_over and not self.rect.collidepoint(event.pos):
                # mouse was on and is leaving the element
                returnval = self.on_mouse_off()
                self.mouse_over = False
                return returnval
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # record where the button was pressed and call on mouse btn down
                returnval = self.set_mouse_btn(event.button, event.pos)
                self.on_mouse_btn_down(event.button)
                return returnval
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.on_mouse_btn_up(event.button)
                if self.get_mouse_btn(event.button):
                    # make sure the button was pressed down on this element
                    return self.on_click(button = event.button, pos = event.pos)
                self.set_mouse_btn(event.button, False)
                return False
        return False
    
    def set_mouse_btn(self, btn, status):
        self.mouse_btn_down[btn] = status
        
    def get_mouse_btn(self, btn):
        if btn in self.mouse_btn_down:
            return self.mouse_btn_down[btn]
        else:
            return False
    
    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect.topleft)
    
    def on_click(self, **kwargs):
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
        
    def on_click(self, **kwargs):
        self.image.fill((255, 255, 255))
    
