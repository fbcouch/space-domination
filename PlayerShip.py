'''
Created on Jul 4, 2012

@author: Jami
'''
from Ship import Ship, PShip


class PlayerShip(Ship):
    '''
    This is an extension of the Ship class that controls the ship via user inputs
    '''


    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None):
        super(PlayerShip,self).__init__(x, y, r, proto, parent, context)
        
        
    def update(self, context = None, timestep = 1.0):
        super(PlayerShip, self).update(context, timestep)
        if context:
            if(context.keys["accel"]): self.accelerate(self.speed * 0.25) 
                
            if(context.keys["brake"]): self.brake(self.speed * 0.25)
            
            if not (context.keys["accel"] or context.keys["brake"]): self.accel = (0,0)
            
            if(context.keys["turnLeft"]): self.set_rotation(self.get_rotation() + 5.0 * timestep)
            if(context.keys["turnRight"]): self.set_rotation(self.get_rotation() - 5.0 * timestep)
            
            if(context.keys["fire"]): 
                bullet = self.fire_weapon(context.timeTotal)
                
                
                if bullet:
                    for bt in bullet:
                        context.physics.addChild(bt)
                        context.foregroundSpriteGroup.add(bt)
                    