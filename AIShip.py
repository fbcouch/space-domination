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
        super(AIShip, self).update(context)
        
        if(context):
            self.faceTarget(context.playerShip)
            
            bullet = self.fire_weapon(context.timeTotal)
                
            if not (bullet is None):
                context.physics.addChild(bullet)
                context.foregroundSpriteGroup.add(bullet)
        
            
    def faceTarget(self, target = None):
        
        if target:
            dx = target.rect.left - self.rect.left
            dy = target.rect.top - self.rect.top
            angle = Vec2(0,0)
            angle.setXY(dx, dy)
            targetAngle = (angle.theta) % 360
            dT = targetAngle - self.get_rotation()
            if dT > 180:
                dT = dT - 360
            elif dT < -180:
                dT += 360
            
            if dT > self.turn: 
                self.set_rotation((self.get_rotation() + self.turn) % 360)
            elif dT < -1 * self.turn:
                self.set_rotation((self.get_rotation() - self.turn) % 360)
            else:
                self.set_rotation(targetAngle)            
            
            