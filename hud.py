'''
Created on Jul 19, 2012

@author: Jami
'''
import Utils

class HUD(object):
    '''
    classdocs
    '''
    hud_bottom = None

    def __init__(self):
        '''
        Constructor
        '''
        self.hud_bottom, rect = Utils.load_image("hud_msg_panel.png", colorkey = -1)
        
    def update(self):
        pass
    
    def draw(self, screen, context = None):
        screen.blit(self.hud_bottom, (0, screen.get_height() - self.hud_bottom.get_height()))
        
        
        if context:
            # ammo
            ammotext = "Ammo: %i/%i" % (int(context.playerShip.weapons[context.playerShip.selected_weapon].cur_ammo), int(context.playerShip.weapons[context.playerShip.selected_weapon].max_ammo))
            # health
            healthtext = "Health: %i/%i" % (int(context.playerShip.health), int(context.playerShip.max_health))
            # shields
            shieldtext = "Shield: %i/%i" % (int(context.playerShip.shields), int(context.playerShip.max_shields))
            
            
            y = screen.get_height() - 150
            screen.blit(context.defaultfont.render(ammotext, 1, (0, 250, 0)), (screen.get_width() - context.defaultfont.size(ammotext)[0] - 10, y))
            
            y += context.defaultfont.size(ammotext)[1] + 2
            
            screen.blit(context.defaultfont.render(healthtext, 1, (0, 250, 0)), (screen.get_width() - context.defaultfont.size(healthtext)[0] - 10, y))
            
            y += context.defaultfont.size(healthtext)[1] + 2
            
            screen.blit(context.defaultfont.render(shieldtext, 1, (0, 250, 0)), (screen.get_width() - context.defaultfont.size(shieldtext)[0] - 10, y))
            
            y += context.defaultfont.size(shieldtext)[1] + 2