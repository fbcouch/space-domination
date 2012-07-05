'''
Created on Jul 4, 2012

@author: Jami
'''
from PhysicsEntity import PhysicsEntity


class Bullet(PhysicsEntity):
    
    parent = None
    ticks_remaining = 0
    damage = 0
    
    def __init__(self):
        super(Bullet, self).__init__()
    
    def update(self, context = None):
        super(Bullet, self).update(context)
        
        self.ticks_remaining -= 1;
        
        if (self.ticks_remaining <= 0 or self.removeSelf):
            self.remove(context)
        
    def remove(self, context = None):
        if(context):
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
    def collide(self, physicsEntity = None, context = None):
        if(physicsEntity and not isinstance(physicsEntity, Bullet)):
            self.remove(context)