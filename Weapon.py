'''
Created on Jul 4, 2012

@author: Jami
'''

class Weapon(object):
    max_ammo = 0
    cur_ammo = 0
    ammo_regen = 0
    fire_rate = 0
    last_fire = 0
    base_damage = 0
    bullet_ticks = 100
    bullet_speed = 20
    
    image = None
    
    def can_fire(self, time):
        if (self.cur_ammo > 0 and time > self.last_fire + self.fire_rate):
            return True
        return False
    
