'''
Created on Jul 19, 2012

@author: Jami
'''
from AIShip import StationShip
import Utils
import consts
import math
import pygame

class HUD(object):
    '''
    classdocs
    '''
    hud_bottom = None
    objective_pointer = None
    target_box_red = None
    target_box_blue = None
    
    panel_lower_left = None
    panel_lower_right = None
    weapon_icon_points = [(12, 4), (12, 52)]
    weapon_bar_points = [(114, 6, 300, 43), (114, 54, 300, 43)]
    
    
    hull_icon = None
    shield_icon = None
    status_icon_points = [(40, 6, 300, 43), (40, 54, 300, 43)]
    status_bar_points = [(142, 6, 300, 43), (142, 54, 300, 43)]
    
    pill_green = None
    pill_green_empty = None
    pill_red = None
    pill_red_empty = None
    pill_yellow = None
    pill_yellow_empty = None
    pill_blue = None
    pill_blue_empty = None
    
    selector = None

    def __init__(self):
        '''
        Constructor
        '''
        self.hud_bottom, rect = Utils.load_image("hud_msg_panel.png", colorkey = -1)
        
        self.target_box_blue = Utils.get_asset('target-box-blue.png')
        self.target_box_red = Utils.get_asset('target-box-red.png')
        
        imagey, rect = Utils.load_image("objective-pointer-yellow.png", colorkey = -1)
        imageg, rect = Utils.load_image("objective-pointer-green.png", colorkey = -1)
        self.objective_pointer = {'destroy': imagey, 'survive': imageg}
        
        self.panel_lower_left = Utils.get_asset('hud-panel-lowerleft.png')
        self.panel_lower_right = Utils.get_asset('hud-panel-lowerright.png')
        
        self.shield_icon = Utils.get_asset('hud-icon-shield.png')
        self.hull_icon = Utils.get_asset('hud-icon-hull.png')
        
        self.pill_green = Utils.get_asset('hud-pill-green.png')
        self.pill_green_empty = Utils.get_asset('hud-pill-green-empty.png')
        self.pill_yellow = Utils.get_asset('hud-pill-yellow.png')
        self.pill_yellow_empty = Utils.get_asset('hud-pill-yellow-empty.png')
        self.pill_red = Utils.get_asset('hud-pill-red.png')
        self.pill_red_empty = Utils.get_asset('hud-pill-red-empty.png')
        self.pill_blue = Utils.get_asset('hud-pill-blue.png')
        self.pill_blue_empty = Utils.get_asset('hud-pill-blue-empty.png')
        self.selector = Utils.get_asset('hud-selector-yellow.png')
        
        
    def update(self):
        pass
    
    def draw(self, screen, context, render, font = None):
        if not font: font = pygame.font.Font(None, 20)
        
        if context:
            # draw glowing balls to point out objectives that are off screen
            self.mark_objectives(screen, context.triggerList, pygame.rect.Rect(-1 * render[0], -1 * render[1], screen.get_width(), screen.get_height()), context.shipSpriteGroup)
            
            # display timer
            self.display_timer(screen, context.elapsedTime, font)
            
            # display unit bars
            self.draw_unit_bars(screen, context.shipSpriteGroup, render, font)
            
            # display health, ammo, shields
            self.display_ship_info(screen, context.playerShip, context.medfont)
            
            # draw objective text
            self.display_objectives(screen, context.triggerList, font)
            
            # draw the chat messages
            self.display_messages(screen, context.messageList)
                
    def display_objectives(self, screen, triggers, font = None):
        if not font: font = pygame.font.Font(None, 20)
        
        primary = []
        secondary = []
        maxwidth = font.size("Secondary Objectives")[0]
        for tg in triggers:
            if tg.type.count("objective-primary") > 0:
                primary.append(tg)
            elif tg.type.count("objective-secondary") > 0:
                secondary.append(tg)
            
            w = font.size(tg.display_text)[0]
            if w > maxwidth: maxwidth = w

        y = 0
        if len(primary) > 0:
            screen.blit(font.render("Primary Objectives:",1,(255,255,0)), (screen.get_width() - maxwidth - 24, y))
            y += 20
            
        for tg in primary:
            tgstr = tg.display_text
            if tg.completed:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            screen.blit(font.render(tgstr,1,color), (screen.get_width() - maxwidth, y))
            y += 20
            
        if (len(secondary) > 0):
            screen.blit(font.render("Secondary Objectives:",1,(255,255,0)), (screen.get_width() - maxwidth - 24, y))
            y += 20
            
        for tg in secondary:
            tgstr = tg.display_text
            if tg.completed:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            screen.blit(font.render(tgstr,1,color), (screen.get_width() - maxwidth, y))
            y += 20
    
    def display_messages(self, screen, messages):
        max_w = 0
        for msg in messages:
            if msg.surface.get_width() > max_w:
                max_w = msg.surface.get_width()
        
        y = 0
        x = (screen.get_width() - max_w) * 0.5
        if screen.get_width() - 1000 < 600 and len(messages) < 2:
            y = 50
            
        for msg in messages:
            screen.blit(msg.surface, (x, screen.get_height() - msg.surface.get_height() - y - 5))
            y += msg.surface.get_height() + 5
            msg.update(messages)
    
    def display_ship_info(self, screen, ship, font = None):
        
        # first display the hud panels
        screen.blit(self.panel_lower_left, (0, screen.get_height() - self.panel_lower_left.get_height()))
        screen.blit(self.panel_lower_right, (screen.get_width() - self.panel_lower_right.get_width(), screen.get_height() - self.panel_lower_right.get_height()))
        
        if not font: font = pygame.font.Font(None, 20)
        
            
        # draw the ship status
        
        # shields
        if ship.max_shields > 0:
            boxes = 10
            box_rect = pygame.rect.Rect(screen.get_width() - self.panel_lower_right.get_width() + self.status_bar_points[0][0],
                                        screen.get_height() - self.panel_lower_left.get_height() + self.status_bar_points[0][1],
                                        self.status_bar_points[0][2], self.status_bar_points[0][3])
            self.draw_boxes(float(ship.shields) / float(ship.max_shields), box_rect, consts.COLOR_BLUE, screen, boxes, True)
            if self.shield_icon:
                screen.blit(self.shield_icon, (screen.get_width() - self.panel_lower_right.get_width() + self.status_icon_points[0][0], 
                                               screen.get_height() - self.panel_lower_right.get_height() + self.status_icon_points[0][1]))
            
        # health
        boxes = 10
        box_rect = pygame.rect.Rect(screen.get_width() - self.panel_lower_right.get_width() + self.status_bar_points[1][0],
                                        screen.get_height() - self.panel_lower_left.get_height() + self.status_bar_points[1][1],
                                        self.status_bar_points[1][2], self.status_bar_points[1][3])
        self.draw_boxes(float(ship.health) / float(ship.max_health), box_rect, consts.COLOR_GREEN, screen, boxes, True)
        
        if self.hull_icon:
            screen.blit(self.hull_icon, (screen.get_width() - self.panel_lower_right.get_width() + self.status_icon_points[1][0], 
                                           screen.get_height() - self.panel_lower_right.get_height() + self.status_icon_points[1][1]))
            
            
        n = 0
        for weapon in ship.weapons:
            if n >= 2: break
            color = (0, 250, 0)
            if n == ship.selected_weapon:
                color = consts.COLOR_YELLOW
                if weapon.cooldown_remaining > 0:
                    color = consts.COLOR_RED
                    
            if weapon.cur_ammo <= 0:
                color = consts.COLOR_RED
                
            if weapon.icon:
                screen.blit(weapon.icon, (self.weapon_icon_points[n][0], screen.get_height() - self.panel_lower_left.get_height() + self.weapon_icon_points[n][1]))
                box_rect = pygame.rect.Rect(self.weapon_bar_points[n][0], screen.get_height() - self.panel_lower_left.get_height() + self.weapon_bar_points[n][1], self.weapon_bar_points[n][2], self.weapon_bar_points[n][3])
                
            if n == ship.selected_weapon and self.selector:
                screen.blit(self.selector, (self.weapon_icon_points[n][0], screen.get_height() - self.panel_lower_left.get_height() + self.weapon_icon_points[n][1]))
                
            
            boxes = weapon.max_ammo
            width = 50#(50 / boxes) * boxes + 1
            self.draw_boxes(float(weapon.cur_ammo) / float(weapon.max_ammo), box_rect, color, screen, boxes, True)
            
            n += 1
    
    def draw_unit_bars(self, screen, shiplist, render, font):
        for sprite in shiplist:
            if not sprite.active:
                continue
            
            if sprite.max_shields > 0:
                r = pygame.rect.Rect(sprite.rect.left + render[0], sprite.rect.bottom + render[1], sprite.original.get_rect().width, 10)
                r.centerx = sprite.rect.centerx + render[0]
                self.draw_boxes(float(sprite.shields) / sprite.max_shields, r, consts.COLOR_BLUE, screen)
            
            if sprite.max_health > 0:
                r = pygame.rect.Rect(sprite.rect.left + render[0], sprite.rect.bottom + render[1] + 11, sprite.original.get_rect().width, 10)
                r.centerx = sprite.rect.centerx + render[0]
                self.draw_boxes(float(sprite.health) / sprite.max_health, r, consts.COLOR_GREEN, screen)
            
            if isinstance(sprite, StationShip):
                for hp in sprite.hard_points:
                    if not hp.active:
                        continue
                    r = pygame.rect.Rect(hp.rect.left + render[0], hp.rect.bottom + render[1], hp.original.get_rect().width, 10)
                    r.centerx = hp.rect.centerx + render[0]
                    self.draw_boxes(float(hp.health) / hp.max_health, r, consts.COLOR_GREEN, screen)
                    
            # draw HUD boxes around these guys
            if not sprite.target_box:
                max_d = sprite.rect.width
                if sprite.rect.height > max_d: max_d = sprite.rect.height
                power = math.log(max_d, 2)
                power = int(math.ceil(power))
                size = 2 ** power
                if sprite.team == sprite.TEAM_DEFAULT_FRIENDLY:
                    sprite.target_box = pygame.transform.scale(self.target_box_blue, (size, size))
                else:
                    sprite.target_box = pygame.transform.scale(self.target_box_red, (size, size))
                
            
            screen.blit(sprite.target_box, (render[0] + sprite.rect.left + (sprite.rect.width - sprite.target_box.get_width()) * 0.5, render[1] + sprite.rect.top + (sprite.rect.height - sprite.target_box.get_height()) * 0.5))
            
                    
    
    def draw_boxes(self, pct, rect, color, screen, num_boxes = 1, draw_unfilled = False):
        w = pct * rect.width
        img = self.pill_green.copy()
        u_img = self.pill_green_empty.copy()
        if color == consts.COLOR_RED:
            img = self.pill_red.copy()
            u_img = self.pill_red_empty.copy()
        elif color == consts.COLOR_YELLOW:
            img = self.pill_yellow.copy()
            u_img = self.pill_yellow_empty.copy()
        elif color == consts.COLOR_BLUE:
            img = self.pill_blue.copy()
            u_img = self.pill_blue_empty.copy()
            
        if num_boxes == 1:
            #if pct > 0:
            #    img = pygame.transform.smoothscale(img, (int(rect.width * pct), rect.height))
            #    screen.blit(img, rect.topleft)
            pygame.gfxdraw.rectangle(screen, pygame.rect.Rect(rect.left - 1, rect.top, rect.width + 1, rect.height), color)
            pygame.gfxdraw.box(screen, pygame.rect.Rect(rect.left, rect.top, w, rect.height), color)
        else:    
            #boxes = int(rect.width / 10)
            boxes = num_boxes
            box_width = math.floor((rect.width) / boxes)
            boxes = int(pct * boxes)
            x = rect.left
            draw_boxes = boxes
            if draw_unfilled:
                draw_boxes = num_boxes
            for i in range(draw_boxes):
                add = 0
                diff = rect.width - num_boxes * box_width
                
                if i >= num_boxes - diff:
                    add = 1
                
                if i < boxes:
                    img = pygame.transform.smoothscale(img, (int(box_width - 1 + add), rect.height))
                    screen.blit(img, (x, rect.top))
                else:
                    u_img = pygame.transform.smoothscale(u_img, (int(box_width - 1 + add), rect.height))
                    screen.blit(u_img, (x, rect.top))
                #pygame.gfxdraw.box(screen, pygame.rect.Rect(x, rect.top, box_width - 1 + add, rect.height), color)
                x += box_width + add
    
    def mark_objectives(self, screen, triggers, rect, shiplist):
        '''draw little balls around the edge of the screen toward the offscreen objectives'''
        
        # TODO change color of marker based on survive/kill
        for tg in triggers:
            for ship in tg.get_attached(shiplist):
                if ship.active and not ship.rect.colliderect(rect):
                    # ok, lets draw this guy
                    # to figure out the position, lets assume a line from rect.center (x1, y1) to tg.parent.rect.center (x2, y2)
                    x1, y1 = rect.center
                    x2, y2 = ship.rect.center
                    draw_loc = None
                    if not x1 == x2 and not y1 == y2:
                        m = float(y2 - y1) / float(x2 - x1)
                        b = y1 - m * x1
                        if y2 >= y1:
                            y_test = rect.top + rect.height
                            result = self.calc_line_y(m, b, y_test)
                            if result >= rect.left and result <= rect.left + rect.width:
                                draw_loc = (result, y_test)
                            elif x2 >= x1:
                                draw_loc = (rect.left + rect.width, self.calc_line_x(m, b, rect.left + rect.width))
                            else:
                                draw_loc = (rect.left, self.calc_line_x(m, b, rect.left))
                        else:
                            y_test = rect.top
                            result = self.calc_line_y(m, b, y_test)
                            if result >= rect.left and result <= rect.left + rect.width:
                                draw_loc = (result, y_test)
                            elif x2 >= x1:
                                draw_loc = (rect.left + rect.width, self.calc_line_x(m, b, rect.left + rect.width))
                            else:
                                draw_loc = (rect.left, self.calc_line_x(m, b, rect.left))
                        
                    elif x1 == x2:
                        # boundary case where x1==x2
                        if y2 >= y1:
                            draw_loc = (x2, rect.top + rect.height)
                        else:
                            draw_loc = (x2, rect.top)
                    else:
                        #boundary case where y1==y2
                        if x2 >= x1:
                            draw_loc = (rect.left + rect.width, y2)
                        else:
                            draw_loc = (rect.left, y2)
                    
                    # draw the damn thing
                    if draw_loc:
                        
                        draw_loc = (draw_loc[0] - rect.left, draw_loc[1] - rect.top)
                        #pygame.gfxdraw.filled_circle(screen, int(draw_loc[0]), int(draw_loc[1]), 10, (255,255,0))
                        draw_rect = self.objective_pointer['destroy'].get_rect()
                        draw_rect.center = draw_loc
                        if tg.condition.count('survive') > 0:
                            screen.blit(self.objective_pointer['survive'], draw_rect.topleft)
                        else:
                            screen.blit(self.objective_pointer['destroy'], draw_rect.topleft)
    
    def display_timer(self, screen, time, font = None):
        #h = int(time / TIME_HRS_MUL)
        #time -= h * TIME_HRS_MUL
        m = int(time / consts.TIME_MIN_MUL)
        time -= m * consts.TIME_MIN_MUL
        s = int(time / consts.TIME_SEC_MUL)
        if s < 10:
            text = "Mission Time %i:0%i" % (m, s)
        else:
            text = "Mission Time %i:%i" % (m, s)
            
        screen.blit(font.render(text, 1, (0, 255, 0)), (10, 10))
            
    def calc_line_x(self, m, b, x):
        return m * x + b
    
    def calc_line_y(self, m, b, y):
        return (y - b) / m