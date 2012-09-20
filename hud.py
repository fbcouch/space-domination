'''
Created on Jul 19, 2012

@author: Jami
'''
import Utils
import consts
import pygame

class HUD(object):
    '''
    classdocs
    '''
    hud_bottom = None
    objective_pointer = None

    def __init__(self):
        '''
        Constructor
        '''
        self.hud_bottom, rect = Utils.load_image("hud_msg_panel.png", colorkey = -1)
        
        
        imagey, rect = Utils.load_image("objective-pointer-yellow.png", colorkey = -1)
        imageg, rect = Utils.load_image("objective-pointer-green.png", colorkey = -1)
        self.objective_pointer = {'destroy': imagey, 'survive': imageg}
        
    def update(self):
        pass
    
    def draw(self, screen, context, render, font = None):
        if not font: font = pygame.font.Font(None, 20)
        
        if context:
            # draw glowing balls to point out objectives that are off screen
            self.mark_objectives(screen, context.triggerList, pygame.rect.Rect(-1 * render[0], -1 * render[1], screen.get_width(), screen.get_height()), context.shipSpriteGroup)
            
            # draw objective text
            self.display_objectives(screen, context.triggerList, font)
            
            # draw the chat messages
            self.display_messages(screen, context.messageList)
            
            # display health, ammo, shields
            self.display_ship_info(screen, context.playerShip, font)
            
            # display timer
            self.display_timer(screen, context.elapsedTime, font)
            
                
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
        y = 0
        for msg in messages:
            screen.blit(msg.surface, (0, screen.get_height() - msg.surface.get_height() - y - 5))
            y += msg.surface.get_height()
            msg.update(messages)
    
    def display_ship_info(self, screen, ship, font = None):
        if not font: font = pygame.font.Font(None, 20)
        # ammo
        ammotext = []
        n = 0
        for weapon in ship.weapons:
            n += 1
            ammotext.append("%i: %s (%i/%i)" % (n, weapon.name, int(weapon.cur_ammo), int(weapon.max_ammo)))
            
        # health
        healthtext = "Health: %i/%i" % (int(ship.health), int(ship.max_health))
        # shields
        shieldtext = "Shield: %i/%i" % (int(ship.shields), int(ship.max_shields))
        
        statstext = []
        accuracy = 0.0
        if ship.stats['shots-fired'] > 0:
            accuracy = int(float(ship.stats['shots-hit'])/float(ship.stats['shots-fired']) * 1000) / 10.0
        statstext.append("Accuracy: %i.%i (%i/%i)" % (int(accuracy), int((accuracy % 1) * 10), ship.stats['shots-hit'], ship.stats['shots-fired']))
        statstext.append("Kills: %i" % ship.stats['kills'])
        statstext.append("Damage dealt: %i" % ship.stats['damage-dealt'])
        statstext.append("Damage taken: %i" % ship.stats['damage-taken'])
        
        
        y = screen.get_height() - 150
        
        screen.blit(font.render(healthtext, 1, (0, 250, 0)), (screen.get_width() - font.size(healthtext)[0] - 10, y))
        
        y += font.size(healthtext)[1] + 2
        
        screen.blit(font.render(shieldtext, 1, (0, 250, 0)), (screen.get_width() - font.size(shieldtext)[0] - 10, y))
        
        y += font.size(shieldtext)[1] + 2
        
        n = 0
        for weapon in ship.weapons:
            color = (0, 250, 0)
            if n == ship.selected_weapon:
                color = (250, 250, 0)
                
            screen.blit(font.render(ammotext[n], 1, color), (screen.get_width() - font.size(ammotext[n])[0] - 10, y))
            y += font.size(ammotext[n])[1] + 2
            n += 1
            
        for text in statstext:
            color = (0, 250, 0)
            screen.blit(font.render(text, 1, color), (screen.get_width() - font.size(text)[0] - 10, y))
            y += font.size(text)[1] + 2
        
    def mark_objectives(self, screen, triggers, rect, shiplist):
        '''draw little balls around the edge of the screen toward the offscreen objectives'''
        
        # TODO change color of marker based on survive/kill
        for tg in triggers:
            for ship in tg.get_attached(shiplist):
                if not ship.rect.colliderect(rect):
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