'''
Created on Aug 20, 2012

@author: Jami
'''
from consts import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH
from gui.basicmenu import BasicTextInput, BasicTextButton, PagedMenu, Label, \
    DropdownSelector, ImageLabel, BasicMenu
from gui.gui import Frame, Element
from profile import Profile
import Utils
import consts
import math
import profile
import pygame

class ProfileMenu(Frame):
    '''handles the display and user manipulations for the profile list and currently selected profile'''
    
    current_profile = None
    profile_list = None
    set_profile_fxn = None
    save_profiles_fxn = None
    
    profile_view = None
    profile_edit = None
    profile_add = None
    profile_delete = None
    profile_shipselect = None
    profile_shipbuy = None
    profile_shipupgrade = None
    
    ship_list = None
    weapon_list = None
    upgrade_list = None
    
    
    def __init__(self, parent, profile, profiles, set_profile, save_profiles, **kwargs):
        '''Constructor'''
        super(ProfileMenu, self).__init__(parent, **kwargs)
        
        self.current_profile = profile
        self.profile_list = profiles
        self.set_profile_fxn = set_profile
        self.save_profiles_fxn = save_profiles
        self.ship_list = kwargs.get('shiplist', [])
        self.weapon_list = kwargs.get('weaponlist', [])
        self.upgrade_list = kwargs.get('upgradelist', [])
        
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
        
        for child in self.children:
            child.set_active(False)
        
        self.profile_view.set_active(True)
        
    def set_profile_edit(self, profile):
        if profile not in self.profile_list:
            self.profile_list.append(profile)
            self.current_profile = profile
            self.set_profile_fxn(self.current_profile)
        
        if not self.profile_edit:
            # create the edit menu
            self.profile_edit = ProfileEdit(self, self.current_profile, self.save_profiles_fxn)
        else:
            # update the edit menu
            self.profile_edit.set_profile(self.current_profile)
        
        if not self.profile_edit in self.children:
            self.add_child(self.profile_edit)
        
        for child in self.children:
            child.set_active(False)
        
        self.profile_edit.set_active(True)
        
    def set_profile_delete(self, profile):
        if not self.profile_delete:
            # create the delete menu
            self.profile_delete = ProfileDelete(self, self.current_profile)
        else:
            # update
            self.profile_delete.set_profile(self.current_profile)
            
        if not self.profile_delete in self.children:
            self.add_child(self.profile_delete)
            
        for child in self.children:
            child.set_active(False)
            
        self.profile_delete.set_active(True)
        
    def set_profile_shipselect(self, profile):
        if not self.profile_shipselect:
            # create the ship selection menu
            self.profile_shipselect = ShipSelectMenu(self, self.ship_list, self.current_profile)
        else:
            self.profile_shipselect.set_profile(self.current_profile)
            
        if not self.profile_shipselect in self.children:
            self.add_child(self.profile_shipselect)
            
        for child in self.children:
            child.set_active(False)
        
        self.profile_shipselect.set_active(True)
        
    def set_profile_shipbuy(self, profile):
        if self.profile_shipbuy:
            self.children.remove(self.profile_shipbuy)
        
        self.profile_shipbuy = ShipBuyMenu(self, self.ship_list, self.weapon_list, self.current_profile)
        if not self.profile_shipbuy in self.children:
            self.add_child(self.profile_shipbuy)
        
        for child in self.children:
            child.set_active(False)
        
        self.profile_shipbuy.set_active(True)
    
    def set_profile_shipupgrade(self, profile):
        if self.profile_shipupgrade:
            self.children.remove(self.profile_shipupgrade)
        
        self.profile_shipupgrade = ShipUpgradeMenu(self, self.current_profile, self.upgrade_list, self.ship_list, self.weapon_list)
        if not self.profile_shipupgrade in self.children:
            self.add_child(self.profile_shipupgrade)
        
        for child in self.children:
            child.set_active(False)
        
        self.profile_shipupgrade.set_active(True)
    
    def delete_profile(self, pf):
        if pf in self.profile_list:
            self.profile_list.remove(pf)
        
        if self.current_profile is pf:
            if len(self.profile_list) > 0:
                self.current_profile = self.profile_list[0]
            else:
                self.current_profile = profile.create_fresh_profile(profiles = self.profile_list)
                self.profile_list.append(self.current_profile)
            self.set_profile_fxn(self.current_profile)
        self.save_profiles_fxn()
        self.set_profile_view(self.current_profile)   
        
    def get_ship_image(self, profile):
        if not profile:
            profile = self.current_profile
            
        if 'ship' in profile and self.ship_list and int(profile['ship']) >= 0 and int(profile['ship']) < len(self.ship_list):
            file = self.ship_list[int(profile['ship'])].file
            image = Utils.load_image(file, -1)[0]
            return image
        return None 
            
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
            
        
            
        items = []
        sel_item = None
        for profile in self.parent.profile_list:
            item = (profile['name'], profile)
            items.append(item)
            if profile is self.profile:
                sel_item = item
                
        items.append(("New profile...", None))
            
         
        btn = BasicTextButton(self, text = "Edit Profile", font = pygame.font.Font(None, 24), callback = self.set_edit_profile)
        btn.rect.topleft = (400, 25)
        
        btn = BasicTextButton(self, text = "Delete Profile", font = pygame.font.Font(None, 24), callback = self.set_delete_profile)
        btn.rect.topleft = (400, 50)
        
        btn = BasicTextButton(self, text= 'Select & Return to Main Menu', callback = self.parent.parent.main_menu_click, font = pygame.font.Font(None, 24))
        #btn.rect.topleft = (0, -btn.rect.height - self.v_pad)
           
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
        
        # display the player's ship
        image = self.parent.get_ship_image(self.profile)
        if image:
            lb = ImageLabel(self, image, rotate = True, angle = 90)
            lb.rect.center = draw_rect.center
        
        btn.rect.bottomright = draw_rect.bottomright
        
        offset_x = (screen.get_rect().width - draw_rect.width) * 0.5
        offset_y = (screen.get_rect().height - draw_rect.height) * 0.5
        for child in self.children:
                child.rect.topleft = (child.rect.left + offset_x, child.rect.top + offset_y)
    
    def select_profile(self, **kwargs):
        pf = kwargs.get('value', None)
        if pf and pf in self.parent.profile_list:
            self.parent.set_profile_view(pf)
        
        if not pf:
            # set up a new profile
            self.parent.set_profile_edit(profile.create_fresh_profile(profiles = self.parent.profile_list))
    
    def set_edit_profile(self):
        self.parent.set_profile_edit(self.profile)
    
    def set_delete_profile(self):
        self.parent.set_profile_delete(self.profile)
    
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
        
        #pygame.gfxdraw.rectangle(screen, pygame.rect.Rect(draw_rect.left - 5, draw_rect.top - 5, draw_rect.width + 10, draw_rect.height + 10), (51, 102, 255))
        
        
        
class ProfileEdit(Frame):
    
    profile = None
    v_pad = 0
    
    callsign_input = None
    save_profiles_fxn = None
    
    def __init__(self, parent, profile, save_profiles, **kwargs):
        '''Constructor'''
        super(ProfileEdit, self).__init__(parent, **kwargs)
        
        self.save_profiles_fxn = save_profiles
        self.profile = profile
        self.v_pad = kwargs.get('v_pad', 5)
        
        self.init()
        
    def init(self):
        '''initializes the view'''
        self.children = []
        
        width = 0
        x = 0
        y = 0
        # callsign edit
        callsign = "newbie"
        if 'name' in self.profile:
            callsign = self.profile['name']
        cl = BasicTextInput(self, label = "Callsign", value = callsign, font = pygame.font.Font(None, 24))
        cl.rect.topleft = (0, 0)
        self.callsign_input = cl
        y = cl.rect.top + cl.rect.height + self.v_pad
        
        # display the player's ship
        image = self.parent.get_ship_image(self.profile)
        if image:
            lb = ImageLabel(self, image, rotate = True, angle = 90)
            
            lb.rect.left = cl.rect.left + (cl.rect.width - lb.rect.width) * 0.5
            dim = lb.rect.height
            if lb.rect.width > dim: dim = lb.rect.width
            lb.rect.top = cl.rect.top + cl.rect.height + self.v_pad + dim - lb.rect.height
            y = lb.rect.top + lb.rect.height + self.v_pad + dim - lb.rect.height
            
        
        
        # ship selector
        bn = BasicTextButton(self, text = "Select Ship...", font = pygame.font.Font(None, 24), callback = self.set_shipselect)
        bn.rect.center = cl.rect.center
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        # buy ship
        bn = BasicTextButton(self, text = "Buy Ship...", font = pygame.font.Font(None, 24), callback = self.set_shipbuy)
        bn.rect.center = cl.rect.center
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        # upgrade ship
        bn = BasicTextButton(self, text = "Upgrade Ship...", font = pygame.font.Font(None, 24), callback = self.set_shipupgrade)
        bn.rect.center = cl.rect.center
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        # save
        bn = BasicTextButton(self, text = "Save Changes", font = pygame.font.Font(None, 24), callback = self.save_profile)
        bn.rect.center = cl.rect.center
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        # cancel
        bn = BasicTextButton(self, text = "Cancel", font = pygame.font.Font(None, 24), callback = self.parent.set_profile_view)
        bn.rect.center = cl.rect.center
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        
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
        
    def set_profile(self, profile):
        self.profile = profile
        self.init()
    
    def save_profile(self):
        self.profile['name'] = self.callsign_input.value
        self.save_profiles_fxn()
        self.parent.set_profile_view()
        
    def set_shipselect(self):
        self.profile['name'] = self.callsign_input.value
        self.save_profiles_fxn()
        self.parent.set_profile_shipselect(self.profile)
        
    def set_shipbuy(self):
        self.profile['name'] = self.callsign_input.value
        self.save_profiles_fxn()
        self.parent.set_profile_shipbuy(self.profile)
    
    def set_shipupgrade(self):
        self.profile['name'] = self.callsign_input.value
        self.save_profiles_fxn()
        self.parent.set_profile_shipupgrade(self.profile)
        
        
class ProfileDelete(Frame):
    profile = None
    v_pad = 0
    
    def __init__(self, parent, profile, **kwargs):
        super(ProfileDelete, self).__init__(parent, **kwargs)
        self.profile = profile
        self.v_pad = kwargs.get('v_pad', 5)
        
        self.init()
    
    def init(self):
        self.children = []
        y = 0
        lb = Label(self, text = "Do you really want to delete profile %s?" % self.profile['name'])
        y += lb.rect.height + self.v_pad
        
        bn = BasicTextButton(self, text = "Yes", callback = self.parent.delete_profile, callback_kwargs = {'pf': self.profile})
        bn.rect.centerx = lb.rect.centerx
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
        
        bn = BasicTextButton(self, text = "Cancel", callback = self.parent.set_profile_view)
        bn.rect.centerx = lb.rect.centerx
        bn.rect.top = y
        y += bn.rect.height + self.v_pad
    
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
    
    def set_profile(self, profile):
        self.profile = profile
        self.init()

class ShipSelectMenu(PagedMenu):
    shiplist = None
    profile = None
    
    def __init__(self, parent, shiplist, profile, **kwargs):
        
        if not 'back_btn_text' in kwargs: kwargs['back_btn_text'] = "< Back"
        if not 'back_btn_callback' in kwargs: kwargs['back_btn_callback'] = self.back_click
        if not 'item_callback' in kwargs: kwargs['item_callback'] = self.ship_click
        self.shiplist = shiplist
        if self.shiplist:
            items = []
            for ship in self.shiplist:
                if ship.player_flyable and str(ship.id) in profile.shiplist: items.append((Utils.load_image(ship.file, -1)[0], ship.id))
            kwargs['items'] = items
        
        super(ShipSelectMenu, self).__init__(parent, **kwargs)
        
        self.profile = profile
        
    def ship_click(self, **kwargs):
        id = kwargs.get('value', 0)
        self.profile['ship'] = id
        self.parent.set_profile_edit(self.profile)
        
    def back_click(self, **kwargs):
        self.parent.set_profile_edit(self.profile)

    def set_profile(self, pf):
        self.profile = pf

class ShipBuyMenu(PagedMenu):
    shiplist = None
    weaponlist = None
    profile = None
    
    selected_ship = None
    
    title_color = None
    desc_color = None
    desc_max_width = 1024
    
    smallfont = None
    
    def __init__(self, parent, shiplist, weaponlist, profile, **kwargs):
        
        if not 'back_btn_text' in kwargs: kwargs['back_btn_text'] = "< Back"
        if not 'back_btn_callback' in kwargs: kwargs['back_btn_callback'] = self.back_click
        if not 'item_callback' in kwargs: kwargs['item_callback'] = self.ship_click
        self.smallfont = kwargs.get('smallfont', pygame.font.Font(None, 16))
    
        self.shiplist = shiplist
        self.weaponlist = weaponlist
        if self.shiplist:
            items = []
            for ship in self.shiplist:
                if ship.player_flyable and str(ship.id) not in profile.shiplist : 
                    items.append((Utils.load_image(ship.file, -1)[0], ship.id))
            kwargs['items'] = items
        
        self.profile = profile
        super(ShipBuyMenu, self).__init__(parent, **kwargs)
        
        self.title_color = kwargs.get('title_color', (255, 255, 100))
        self.desc_color = kwargs.get('desc_color', (200, 200, 200))
        self.desc_max_width = int(kwargs.get('desc_width', 1024))
        
        
        
        
    def draw(self):
        '''draws the ship selection'''
        draw_rect = super(ShipBuyMenu, self).draw()
        screen = pygame.display.get_surface()
        
        # draw the credit label
        cr_text = "Credit Balance: $%s" % self.profile['credits']
        size = self.font.size(cr_text)
        color = (255, 255, 255)
        if self.selected_ship and int(self.selected_ship.cost) > int(self.profile['credits']):
            color = (255, 0, 0)
        screen.blit(self.font.render(cr_text, 1, color), (draw_rect.right - size[0], draw_rect.top - size[1]))
        
        
        if self.selected_ship:
            y = draw_rect.bottom + self.v_pad * 3
            size = self.font.size(self.selected_ship.name)
            x = (screen.get_width() - size[0]) * 0.5
            screen.blit(self.font.render("%s ($%i)" % (self.selected_ship.name, self.selected_ship.cost), 1, self.title_color), (x, y))
            if x < draw_rect.left: draw_rect.left = x
            y += size[1] + self.v_pad
            
            stats = ["Health %i (%.1f)" % (self.selected_ship.health, self.selected_ship.hregen),
                     "Shields %i (%.1f)" % (self.selected_ship.shields, self.selected_ship.sregen),
                     "Armor %i" % self.selected_ship.armor,
                     "Speed %i" % self.selected_ship.speed,
                     "Turn %i" % self.selected_ship.turn]
            s_max_x = 0
            for s in stats:
                size = self.font.size(s)
                if size[0] > s_max_x: s_max_x = size[0]
            
            weapons = []
            i = 0
            for wpdict in self.selected_ship.weapons:
                i += 1
                wp = self.weaponlist[int(wpdict['id'])]
                weapons.append("(%i) %s" % (i, wp.name))
                weapons.append("  Ammo %i (%.1f)" % (wp.max_ammo, wp.ammo_regen))
                weapons.append("  Damage (Fire Rate) %i (%i)" % (wp.base_damage, wp.fire_rate))
                weapons.append("  Range (Speed) %i (%.1f)" % ((wp.bullet_speed * wp.bullet_ticks), wp.bullet_speed))
                
            x = screen.get_width() * 0.5 - s_max_x - self.h_pad
            y_start = y
            if x < draw_rect.left: draw_rect.left = x
            for s in stats:
                screen.blit(self.font.render(s, 1, self.desc_color), (x, y))
                y += self.v_pad + self.font.size(s)[1]
            
            x = screen.get_width() * 0.5 + self.h_pad
            y = y_start
            screen.blit(self.font.render("Weapons:", 1, self.desc_color), (x, y))
            y += self.v_pad + self.font.size("Weapons:")[1]
            y_start = y
            i = 0
            max_x = 0
            x -= self.h_pad
            for w in weapons:
                if i % (len(weapons) / len(self.selected_ship.weapons)) == 0:
                    x += max_x + self.h_pad
                    y = y_start
                screen.blit(self.smallfont.render(w, 1, self.desc_color), (x, y))
                size = self.smallfont.size(w)
                y += self.v_pad + size[1]
                if x + size[0] > draw_rect.right:
                    draw_rect.width = x + size[0] - draw_rect.left
                if size[0] > max_x: max_x = size[0]
                i += 1
            draw_rect.height = y - draw_rect.top
        return draw_rect
            
        
    def ship_click(self, **kwargs):
        id = kwargs.get('value', 0)
        if int(self.profile['credits']) >= int(self.shiplist[id].cost):
            self.profile['credits'] = int(self.profile['credits']) - int(self.shiplist[id].cost)
            self.profile.shiplist[str(id)] = {'id': id, 'upgrades': ''}
            self.parent.set_profile_edit(self.profile)
        
        
    def back_click(self, **kwargs):
        self.parent.set_profile_edit(self.profile)

    def set_profile(self, pf):
        self.profile = pf
        
    def mouse_over_callback(self, child):
        if self.selected_item and self.selected_item is not child:
            self.selected_item.on_mouse_off()
            
        self.selected_ship = self.find_ship(child.callback_kwargs.get('value', None))
        self.selected_item = child
        
    def find_ship(self, id):
        if id is None: return None
        
        for ship in self.shiplist:
            if ship.id == id:
                return ship
            
        return None
        
class ShipUpgradeMenu(Frame):    
    upgradelist = None
    shiplist = None
    weaponlist = None
    profile = None
    
    healthLabel = None
    shieldLabel = None
    armorLabel = None
    speedLabel = None
    weaponLabel = None
    
    healthButton = None
    shieldButton = None
    armorButton = None
    speedButton = None
    weaponButton = None
    
    backButton = None
    creditLabel = None
    
    shipImage = None
    
    width = 600
    height = 300
    
    def __init__(self, parent, profile, upgradelist, shiplist, weaponlist, **kwargs):
        super(ShipUpgradeMenu, self).__init__(parent, **kwargs)
        self.profile = profile
        self.shiplist = shiplist
        self.upgradelist = upgradelist
        self.weaponlist = weaponlist
        
        self.backButton = BasicTextButton(self, text = '< Back', callback = self.back_click)
        self.backButton.rect.topleft = (0, 0)
        
        self.creditLabel = Label(self, "Credits $%i" % int(self.profile['credits']))
        self.creditLabel.rect.topright = (self.width, 0)
        
        self.shipImage = ImageLabel(self, self.shiplist[int(profile['ship'])].image, rotate = True)
        max_d = self.shipImage.image.get_width()
        if self.shipImage.image.get_height() > max_d:
            max_d = self.shipImage.image.get_height()
        self.shipImage.rect.center = (self.width * 0.5, max_d * 0.5)
        y = max_d + 5
        
        self.healthLabel = Label(self, "Health %i (%.1f)")
        self.healthLabel.rect.topleft = (0, y)
        
        self.healthButton = BasicTextButton(self, text = "+", callback = self.upgrade_click, callback_kwargs = {})
        self.healthButton.rect.topleft = (self.width * 0.5, y)
        y = self.healthButton.rect.bottom + 5
        
        self.shieldLabel = Label(self, "Shield %i (%.1f)")
        self.shieldLabel.rect.topleft = (0, y)
        
        self.shieldButton = BasicTextButton(self, text = "+", callback = self.upgrade_click, callback_kwargs = {})
        self.shieldButton.rect.topleft = (self.width * 0.5, y)
        y = self.shieldButton.rect.bottom + 5
        
        self.armorLabel = Label(self, "Armor %i")
        self.armorLabel.rect.topleft = (0, y)
        
        self.armorButton = BasicTextButton(self, text = "+", callback = self.upgrade_click, callback_kwargs = {})
        self.armorButton.rect.topleft = (self.width * 0.5, y)
        y = self.armorButton.rect.bottom + 5
        
        self.speedLabel = Label(self, "Speed (Turn) %i (%.1f)")
        self.speedLabel.rect.topleft = (0, y)
        
        self.speedButton = BasicTextButton(self, text = "+", callback = self.upgrade_click, callback_kwargs = {})
        self.speedButton.rect.topleft = (self.width * 0.5, y)
        y = self.speedButton.rect.bottom + 5
        
        self.weaponLabel = Label(self, "Damage %i / %i")
        self.weaponLabel.rect.topleft = (0, y)
        
        #self.weaponButton = BasicTextButton(self, text = "+")
        #self.weaponButton.rect.topleft = (self.width * 0.5, y)
        #y = self.weaponButton.rect.bottom + 5
        
        
        offset = ((pygame.display.get_surface().get_width() - self.width) * 0.5, (pygame.display.get_surface().get_height() - self.height) * 0.5)
        for c in self.children:
            c.rect.topleft = (c.rect.left + offset[0], c.rect.top + offset[1])
        
        self.update_elements()
        
    def update_elements(self):
        ship = self.shiplist[int(self.profile['ship'])]
        upgrades = Utils.parse_intlist(self.profile.shiplist[str(self.profile['ship'])]['upgrades'])
        wp_dmg = []
        for w in ship.weapons:
            wp_dmg.append(self.weaponlist[int(w['id'])].base_damage)
                
        for up in upgrades:
            upgrade = self.upgradelist[up]
            ship.health += upgrade.health
            ship.hregen += upgrade.hregen
            ship.shields += upgrade.shields
            ship.sregen += upgrade.sregen
            ship.armor += upgrade.armor
            ship.speed += upgrade.speed
            ship.turn += upgrade.turn
            
            for w in wp_dmg:
                w += upgrade.damage
                
            
        if len(wp_dmg) < 2:
            wp_dmg.append(-1)
        
        if len(wp_dmg) < 2:
            wp_dmg.append(-1)
        
        self.healthLabel.set_text(self.healthLabel.text % (ship.health, ship.hregen))
        self.shieldLabel.set_text(self.shieldLabel.text % (ship.shields, ship.sregen))
        self.armorLabel.set_text(self.armorLabel.text % ship.armor)
        self.speedLabel.set_text(self.speedLabel.text % (ship.speed, ship.turn))
        self.weaponLabel.set_text(self.weaponLabel.text % (wp_dmg[0], wp_dmg[1]))
        
        
        h_upgrade = None
        s_upgrade = None
        a_upgrade = None
        p_upgrade = None
        # figure out what options to allow the user to buy
        for up in self.upgradelist:
            if not int(self.profile['ship']) in up.fits:
                # this doesnt fit, skip it
                continue
            if not h_upgrade and up.type.count('health') > 0:
                h_upgrade = up
            if not s_upgrade and up.type.count('shield') > 0:
                s_upgrade = up
            if not a_upgrade and up.type.count('armor') > 0:
                a_upgrade = up
            if not p_upgrade and up.type.count('speed') > 0:
                p_upgrade = up
                
        if h_upgrade:
            self.healthButton.callback_kwargs['value'] = h_upgrade
            self.healthButton.set_text("$%i: +%i (+%.1f)" % (h_upgrade.cost, h_upgrade.health, h_upgrade.hregen))
        if s_upgrade:
            self.shieldButton.callback_kwargs['value'] = s_upgrade
            self.shieldButton.set_text("$%i: +%i (+%.1f)" % (s_upgrade.cost, s_upgrade.shields, s_upgrade.sregen))
        if a_upgrade:
            self.armorButton.callback_kwargs['value'] = a_upgrade
            self.armorButton.set_text("$%i: +%i" % (a_upgrade.cost, a_upgrade.armor))
        if p_upgrade:
            self.speedButton.callback_kwargs['value'] = p_upgrade
            self.speedButton.set_text("$%i: +%i (+%.1f)" % (p_upgrade.cost, p_upgrade.speed, p_upgrade.turn))
            
            
        
        
    def draw(self):
        super(ShipUpgradeMenu, self).draw()
        
    def back_click(self, **kwargs):
        self.parent.set_profile_edit(self.profile)
    
    def upgrade_click(self, **kwargs):
        pass
#   . 
#     .
# . . .
