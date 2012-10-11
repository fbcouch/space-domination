'''
Created on Jul 4, 2012

@author: Jami
'''
from Particle import Particle, GlowParticle
from PhysicsEntity import PhysicsEntity
from Utils import load_sprite_sheet
from Vec2 import Vec2
import Utils
import pygame


class Bullet(PhysicsEntity):
    
    parent = None
    ticks_remaining = 0.0
    damage = 0
    type = "laser"
    
    blip_time = 0.0
    
    def __init__(self):
        super(Bullet, self).__init__()
    
    def update(self, context = None, timestep = 1):
        super(Bullet, self).update(context)
        
        self.ticks_remaining -= timestep;
        
        
        self.blip_time += timestep
        if self.blip_time > 10:
            self.blip_time = 10
        if self.engine_points and (self.accel[0] != 0 or self.accel[1] != 0) and self.blip_time > 1:
            self.blip_time -= 1
            for ep in self.engine_points:
                #engine_glow = Particle(load_sprite_sheet('glowengine1_10.png', 10, 10, colorkey = -1), interval = 1)
                engine_glow = GlowParticle('circle', 10, self.engine_color, 100, interval = 1)
                
                offset = Vec2(0,0)
                offset.setXY(ep[0] - 0.5 * self.original.get_rect().width, ep[1] - 0.5 * self.original.get_rect().height)
                offset.theta += self.rotation
                offset = offset.getXY()
                engine_glow.rect.center = (self.rect.center[0] + offset[0], self.rect.center[1] + offset[1])
                engine_glow.set_rotation(self.rotation)
                context.foregroundSpriteGroup.add(engine_glow)
        
        if self.removeSelf:
            self.remove(context)
        if (self.ticks_remaining <= 0):
            if self.type == 'missile':
                explosion = Particle(Utils.get_asset('explosion3.png'), target = self)
                context.foregroundSpriteGroup.add(explosion)
            self.remove(context)
                
        
    def remove(self, context = None):
        if(context):
            if self in context.physics.physicsChildren: context.physics.physicsChildren.remove(self)
            if self in context.foregroundSpriteGroup: context.foregroundSpriteGroup.remove(self)
            
    def collide(self, physicsEntity = None, context = None):
        
        if(physicsEntity and not isinstance(physicsEntity, Bullet)):
            
            if physicsEntity.health < physicsEntity.max_health and physicsEntity.shields <= 1:
                explosion = Particle(Utils.get_asset('explosion3.png'), target = self)
                context.foregroundSpriteGroup.add(explosion)
            else:
                # sheild hit
                explosion = Particle(Utils.get_asset('shield_hit.png'), target = self)
                context.foregroundSpriteGroup.add(explosion)
            self.parent.stats['damage-dealt'] += self.damage
            self.parent.stats['shots-hit'] += 1
            self.remove(context)