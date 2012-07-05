'''
Created on Jul 4, 2012

@author: Jami
'''
from Ship import Ship, PShip
from Vec2 import Vec2

class AIShip(Ship):
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None):
        super(AIShip,self).__init__(x, y, r, proto, parent)
        
    def update(self, context = None):
        #face the playerShip!
        
        if(context):
            self.faceTarget(context.playerShip)
            
            bullet = self.fire_weapon(context.timeTotal)
                
            if not (bullet is None):
                context.physics.addChild(bullet)
                context.foregroundSpriteGroup.add(bullet)
        
            
    def faceTarget(self, target = None):
        
        if target:
            dx = self.rect.left - target.rect.left
            dy = self.rect.top - target.rect.top
            angle = Vec2(0,0)
            angle.setXY(dx, dy)
            targetAngle = (angle.theta + 180) % 360
            dT = self.get_rotation() - targetAngle + 180
            
            print str(dT) # TODO make this turn over time rather than instantaneously facing target
            #if dT > self.turn: self.set_rotation((self.get_rotation() + self.turn) % 360)
            #elif dT < -1 * self.turn: self.set_rotation((self.get_rotation() - self.turn) % 360)
            #else: 
            self.set_rotation(targetAngle)
            
            