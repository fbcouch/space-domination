'''
Created on Aug 20, 2012

@author: Jami
'''
from consts import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from gui.gui import Frame, Element
from profile import Profile
import Utils
import consts
import math
import pygame

class ProfileMenu(Frame):
    '''handles the display and user manipulations for the profile list and currently selected profile'''
    
    current_profile = None
    profile_list = None
    set_profile_fxn = None
    
    profile_view = None
    profile_edit = None
    profile_add = None
    profile_delete = None
    
    ship_list = None
    
    
    def __init__(self, parent, profile, profiles, set_profile, **kwargs):
        '''Constructor'''
        super(ProfileMenu, self).__init__(parent, **kwargs)
        
        self.current_profile = profile
        self.profile_list = profiles
        self.set_profile_fxn = set_profile
        self.ship_list = kwargs.get('shiplist', [])
        
        self.set_profile_view(self.current_profile)
    
    def update(self, event):
        '''updates the menu based on the event'''
        returnVal = super(ProfileMenu, self).update(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.parent.main_menu_click()
        
        return returnVal
        
    def draw(self):
        super(ProfileMenu, self).draw()
        
    def set_profile_view(self, profile = None):
        if profile and profile is not self.current_profile and profile in self.profile_list:
            self.current_profile = profile
            self.set_profile_fxn(self.current_profile)
        
        if not self.profile_view:
            # create the menu anew:
            self.profile_view = ProfileView(self, self.current_profile)
        else:
            # update the current view menu
            self.profile_view.set_profile(self.current_profile)
            
        if not self.profile_view in self.children:
            self.add_child(self.profile_view)
        
        self.profile_view.set_active(True)
        
    def set_profile_edit(self, profile):
        if profile not in self.profile_list:
            self.profile_list.append(profile)
            self.current_profile = profile
            self.set_profile_fxn(self.current_profile)
        
        if not self.profile_edit:
            # create the edit menu
            self.profile_edit = ProfileEdit(self, self.current_profile)
        else:
            # update the edit menu
            self.profile_edit.set_profile(self.current_profile)
        
        if not self.profile_edit in self.children:
            self.add_child(self.profile_edit)
        
        self.profile_view.set_active(True)
            
class ProfileView(Frame):
    '''handles the display of the current profile'''
    
    profile = None
    v_pad = 0
    
    def __init__(self, parent, profile, **kwargs):
        '''Constructor'''
        super(ProfileView, self).__init__(parent, **kwargs)
        self.profile = profile
        self.v_pad = kwargs.get('v_pad', 5)
        
        self.init()
        
    def init(self):
        '''initializes the view'''
        
        width = 0
        x = 0
        y = 0
        self.children = []
        lb = Label(self, "Callsign: %s" % self.profile['name'])
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
        
        if not 'shots-fired' in self.profile:
            self.profile['shots-fired'] = 0
        if not 'shots-hit' in self.profile:
            self.profile['shots-hit'] = 0
        if not 'kills' in self.profile:
            self.profile['kills'] = 0
        if not 'deaths' in self.profile:
            self.profile['deaths'] = 0
        if not 'damage-dealt' in self.profile:
            self.profile['damage-dealt'] = 0
        if not 'damage-taken' in self.profile:
            self.profile['damage-taken'] = 0
        
        if int(self.profile['deaths']) > 0:
            ratio = float(self.profile['kills']) / float(self.profile['deaths'])
        else:
            ratio = float(self.profile['kills'])
        ratio_dec = int((ratio - int(ratio)) * 10)
        lb = Label(self, "Kills: %i" % int(self.profile['kills']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
        
        lb = Label(self, "Deaths: %i" % int(self.profile['deaths']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
        
        lb = Label(self, "K/D Ratio: %i.%i" % (int(ratio), int(ratio_dec)))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        if float(self.profile['shots-fired']) > 0:
            accuracy = float(self.profile['shots-hit']) / float(self.profile['shots-fired']) * 100
        else:
            accuracy = 0.0
        accuracy_dec = int((accuracy - int(accuracy)) * 10)
        
        lb = Label(self, "Shots Hit: %i" % int(self.profile['shots-hit']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        lb = Label(self, "Shots Fired: %i" % int(self.profile['shots-fired']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        lb = Label(self, "Accuracy: %i.%i" % (int(accuracy), accuracy_dec))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        lb = Label(self, "Damage Dealt: %i" % int(self.profile['damage-dealt']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        lb = Label(self, "Damage Taken: %i" % int(self.profile['damage-taken']))
        lb.rect.topleft = (x, y)
        y += lb.rect.height + self.v_pad
        if lb.rect.width > width:
            width = lb.rect.width
            
        # display the player's ship
        if 'ship' in self.profile and self.parent.ship_list and int(self.profile['ship']) > 0 and int(self.profile['ship']) < len(self.parent.ship_list):
            file = self.parent.ship_list[int(self.profile['ship'])].file
            image = Utils.load_image(file, -1)[0]
            lb = ImageLabel(self, image, rotate = True, angle = 90)
            lb.rect.center = (width + lb.rect.width, (y - self.v_pad) // 2)
            width += lb.rect.width * 2
            
        items = []
        sel_item = None
        for profile in self.parent.profile_list:
            item = (profile['name'], profile)
            items.append(item)
            if profile is self.profile:
                sel_item = item
                
        items.append(("New profile...", Profile()))
            
            
        ds = DropdownSelector(self, items, sel_item, on_select = self.select_profile)
        ds.rect.topleft = (400, 0)
            
        screen = pygame.display.get_surface()
        
        draw_rect = pygame.rect.Rect(0, 0, 0, 0)
        for child in self.children:
            if child.is_active():
                if child.rect.left + child.rect.width > draw_rect.width:
                    draw_rect.width = child.rect.left + child.rect.width
                if child.rect.top + child.rect.height > draw_rect.height:
                    draw_rect.height = child.rect.top + child.rect.height
                    
        offset_x = (screen.get_rect().width - draw_rect.width) * 0.5
        offset_y = (screen.get_rect().height - draw_rect.height) * 0.5
        for child in self.children:
                child.rect.topleft = (child.rect.left + offset_x, child.rect.top + offset_y)
    
    def select_profile(self, **kwargs):
        profile = kwargs.get('value', None)
        if profile and profile in self.parent.profile_list:
            self.parent.set_profile_view(profile)
        elif profile:
            self.parent.set_profile_edit(profile)
            
    
    def set_profile(self, profile):
        self.profile = profile
        self.init()
        
    def get_profile(self):
        return self.profile
    
    def draw(self):
        screen = pygame.display.get_surface()
        
        draw_rect = None #pygame.rect.Rect(0, 0, 0, 0)
        for child in self.children:
            if child.is_active():
                if not draw_rect:
                    draw_rect = child.rect.copy()
                if child.rect.left < draw_rect.left:
                    draw_rect.width += draw_rect.left - child.rect.left
                    draw_rect.left = child.rect.left
                if child.rect.top < draw_rect.top:
                    draw_rect.height += draw_rect.top - child.rect.top
                    draw_rect.top = child.rect.top
                if child.rect.left + child.rect.width > draw_rect.left + draw_rect.width:
                    draw_rect.width = (child.rect.left + child.rect.width) - draw_rect.left
                if child.rect.top + child.rect.height > draw_rect.top + draw_rect.height:
                    draw_rect.height = (child.rect.top + child.rect.height) - draw_rect.top
                    
        offset_x = (screen.get_rect().width - draw_rect.width) * 0.5
        offset_y = (screen.get_rect().height - draw_rect.height) * 0.5
        '''for child in self.children:
            if child.is_active():
                save_rect = child.rect.copy()
                child.rect.topleft = (child.rect.left + offset_x, child.rect.top + offset_y)
                child.draw()
                child.rect.center = save_rect.center'''
        for child in self.children:
            if child.is_active():
                child.draw()
        
        pygame.gfxdraw.rectangle(screen, pygame.rect.Rect(draw_rect.left - 5, draw_rect.top - 5, draw_rect.width + 10, draw_rect.height + 10), (51, 102, 255))
        
class ProfileEdit(Frame):
    
    profile = None
    v_pad = 0
    
    def __init__(self, parent, profile, **kwargs):
        '''Constructor'''
        super(ProfileEdit, self).__init__(parent, **kwargs)
        
        self.profile = profile
        self.v_pad = kwargs.get('v_pad', 50)
        
        self.init()
        
    def init(self):
        '''initializes the view'''
        
        width = 0
        x = 0
        y = 0



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
#   . 
#     .
# . . .
