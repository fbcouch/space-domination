'''
Created on Jul 4, 2012

@author: Jami
'''
from Bullet import Bullet
from PhysicsEntity import PhysicsEntity
from Ship import Ship, PShip
from Vec2 import Vec2
import consts
import math
import pygame
import random

DIFFICULTY_HARD = 0
DIFFICULTY_NORMAL = 1
DIFFICULTY_EASY = 2
DEFAULT_AREA_SIZE = 500

FORMATION_DEFAULT = [(0,0), (-200, -200), (-200, 200), (-400, -400), (-400, 400), (-400, 0)]



class AIShip(Ship):
    home_position = None
    waypoint = None
    area_size = DEFAULT_AREA_SIZE
    max_facing_angle = 5
    
    squad = None
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None, squad = None):
        super(AIShip,self).__init__(x, y, r, proto, parent, context)
        
        self.squad = squad
        self.home_position = (x, y)
        
        if len(self.weapons) > 0 and self.selected_weapon < len(self.weapons):
            self.area_size = self.weapons[self.selected_weapon].bullet_speed * self.weapons[self.selected_weapon].bullet_ticks
        self.waypoint = self.update_waypoint()
        
    def update(self, context = None, timestep = 1):
        super(AIShip, self).update(context, timestep)
        if not self.active:
            return
            
        if self.removeSelf and self.squad:
            self.squad.remove(self)
            self.squad = None
        
        if not self.target or self.target.health <= 0:
            self.find_target(context.shipSpriteGroup)
        
        self.engine_color = consts.COLOR_BLUE
        
        collide = False
        if self.collider:
            collide = self.will_collide(self.collider)
        
        if collide: 
            collide = self.collider
            self.engine_color = consts.COLOR_RED
            x, angle = self.get_angle_to_target(self.collider.rect.center)
            dist = self.distance_to_sq(self.collider.rect)
            
            
            if angle >= 0:
                # turn right
                self.set_rotation((self.get_rotation() - self.turn * timestep) % 360)
            else:
                # turn left
                self.set_rotation((self.get_rotation() + self.turn * timestep) % 360)
        
            #if dist < self.get_vel_sq() * consts.COLLIDE_TICKS ** 2 * 0.5 and math.fabs(angle) < 45:
            #    # stop
            #    self.brake(self.speed * 0.5)

            #accelerate toward target
            self.accelerate(self.speed * 0.25)
                
                
                
        elif context and self.target and len(self.weapons) > 0 and self.distance_to_sq(self.target.rect) < self.area_size * self.area_size:
            # we are near the target - face & attack it!
            target = self.target.rect.center
            # adjust for the velocity of the target and the distance to it
            dist = math.sqrt(self.distance_to_sq(self.target.rect))
            time = float(dist) / float(self.weapons[self.selected_weapon].bullet_speed)
            target = (target[0] + self.target.velocity[0] * time, target[1] + self.target.velocity[1] * time)
            
            if self.squad:
                if self.squad.is_leader(self):
                    self.squad.squad_target = target
                self.waypoint = self.squad.get_target_position(self)
            else:
                self.waypoint = target
            
            # TODO next add a bit of noise to account for difficulty
            if not self.waypoint:
                self.waypoint = self.update_waypoint()
            angle = self.face_target(self.waypoint, timestep)
            
            x, angle = self.get_angle_to_target(target)
            
            bullet = None
            
            # don't fire unless we're facing the target
            if math.fabs(angle) < self.max_facing_angle: 
                # test whether an ally is within the line of fire
                vel = Vec2(self.weapons[self.selected_weapon].bullet_speed, self.rotation)
                
                can_fire = True
                for ship in context.shipSpriteGroup:
                    # create a small rect to calculate the bullet trajectory
                    test_bullet = PhysicsEntity()
                    test_bullet.rect = pygame.rect.Rect(self.rect.center[0], self.rect.center[1], 1, 1)
                    test_bullet.velocity = vel.getXY()
                    
                    if ship is self or ship is self.parent:
                        # we don't care if the bullet intersects with self or parent
                        continue
                    if not ship.team == self.team:
                        # we don't mind hitting an enemy
                        continue
                    if test_bullet.will_collide(ship): # TODO take into account the bullet lifetime here
                        # we would hit a friendly...
                        can_fire = False
                if can_fire:
                    bullet = self.fire_weapon(context.timeTotal)
                
            if bullet:
                for bt in bullet:
                    context.physics.addChild(bt)
                    context.foregroundSpriteGroup.add(bt)
            
            # accelerate toward target
            self.accelerate(self.speed * 0.25)
                
        else:
            if self.rect.collidepoint(self.waypoint):
                self.waypoint = self.update_waypoint()
                
            if self.squad:
                if self.squad.is_leader(self):
                    self.squad.squad_target = self.waypoint
                self.waypoint = self.squad.get_target_position(self)
                
            
            # we are not near the target (or didn't give a context)
            save_angle = self.get_rotation()
            self.face_target(self.waypoint, timestep)
            if self.collider and self.will_collide(self.collider):
                self.set_rotation(save_angle)
            
            # accelerate toward target
            self.accelerate(self.speed * 0.25)
            
            
    def face_target(self, target, timestep = 1):
        
        targetAngle, dT = self.get_angle_to_target(target)
        
        
        if dT > self.turn * timestep: 
            self.set_rotation((self.get_rotation() + self.turn * timestep) % 360)
        elif dT < -1 * self.turn * timestep:
            self.set_rotation((self.get_rotation() - self.turn * timestep) % 360)
        else:
            self.set_rotation(targetAngle)
            
        return dT
    
    def get_angle_to_target(self, target):
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        angle = Vec2(0,0)
        angle.setXY(dx, dy)
        targetAngle = (angle.theta) % 360
        
        dT = targetAngle - self.get_rotation()
        if dT > 180:
            dT = dT - 360
        elif dT < -180:
            dT += 360
            
        return targetAngle, dT
            
    def update_waypoint(self):
        return (self.home_position[0] + random.randint(-1 * self.area_size, self.area_size), self.home_position[1] + random.randint(-1 * self.area_size, self.area_size))
        
    def consider_target(self, target):
        if not (isinstance(target, Ship) or isinstance(target, AIShip)):
            return False
        
        if not target.team == self.team:
            if not self.target or self.target.health <= 0 or self.distance_to_sq(self.target.rect) > self.distance_to_sq(target.rect):
                self.target = target
                return True
        return False
    
    
    def find_target(self, shipList):
        closest = None
        for ship in shipList:
            if not ship.team == self.team:
                if not closest or self.distance_to_sq(closest.rect) > self.distance_to_sq(ship.rect):
                    closest = ship
        self.target = closest
                

class StationShip(AIShip):
    
    initialized = False
    
    def __init__(self, x = 0, y = 0, r = 0, proto = PShip(), parent = None, context = None):
        super(StationShip,self).__init__(x, y, r, proto, parent, context)
        self.home_position = (x, y)
        self.waypoint = (x, y)
        self.area_size = 500
        
    def update(self, context = None, timestep = 1):
        super(AIShip, self).update(context, timestep)
        if not self.active:
            return False
        
        if not self.initialized:
            for hp in self.hard_points:
                hp.area_size = hp.weapons[0].bullet_speed * hp.weapons[0].bullet_ticks
                if hp.area_size > self.area_size: self.area_size = hp.area_size
            self.initialized = True
        
        if context and self.target:
            if self.distance_to_sq(self.target.rect) < self.area_size * self.area_size:
                for hp in self.hard_points:
                    hp.waypoint = self.target.rect.center
                    hp.target = self.target
            
        
    def can_collide(self, physicsEntity):
        if not super(StationShip, self).can_collide(physicsEntity):
            return False
        
        if len(self.hard_points) == 0 or self.shields > 0:
            return True
        else:
            for hp in self.hard_points:
                if hp.rect.colliderect(physicsEntity.rect):
                    if pygame.sprite.collide_mask(hp, physicsEntity):
                        
                        return True # it's hitting a hard point, collide!
            
            
            # special case: there are hard points and we can collide
            # if the collision is going to hit a hard point eventually, leave it alone
            # otherwise, go ahead and collide
            if isinstance(physicsEntity, Bullet):
                # if it's a bullet, it has "ticks_remaining"
                ticks = physicsEntity.ticks_remaining
            elif physicsEntity.get_vel_sq() == 0:
                ticks = 0
            else:
                ticks = int(math.sqrt(self.rect.width * self.rect.width + self.rect.height * self.rect.height) / math.sqrt(physicsEntity.get_vel_sq())) + 1
            
            for hp in self.hard_points:
                if physicsEntity.will_collide(hp): # TODO implement ticks
                    return False
            return True
        
    def collide(self, physicsEntity = None, context = None):
        hit_hp = None
        for hp in self.hard_points:
            if hp.rect.colliderect(physicsEntity.rect):
                if pygame.sprite.collide_mask(hp, physicsEntity):
                    hit_hp = hp
        
        if hit_hp:
            hit_hp.collide(physicsEntity, context)
        else:
            return super(StationShip, self).collide(physicsEntity, context)
        
    def consider_target(self, target):
        if not (isinstance(target, Ship) or isinstance(target, AIShip)):
            return False
        
        if not target.team == self.team:
            if not self.target or self.target.health <= 0 or self.distance_to_sq(self.target.rect) > self.distance_to_sq(target.rect):
                self.target = target
                return True
        return False
    
class Squadron(object):
    ships = None
    angle = None
    squad_target = None
    formation = None
    
    def __init__(self):
        self.ships = []
        self.angle = 0
        self.squad_target = (0, 0)
        self.formation = FORMATION_DEFAULT
    
    def append(self, ship):
        if not ship in self.ships:
            self.ships.append(ship)
            
    def remove(self, ship):
        if ship in self.ships:
            self.ships.remove(ship)
    
    def get_target_position(self, ship):
        if ship in self.ships and self.ships.index(ship) == 0:
            # if we are the leader
            
            return self.squad_target
        elif ship in self.ships:
            # not the leader
            # TODO calculate the target position from the squad formation and position in the squad
            i = self.ships.index(ship)
            if i < len(self.formation):
                angle = self.ships[0].get_rotation()
                offset = Vec2(0, 0)
                offset.setXY(self.formation[i][0], self.formation[i][1])
                offset.theta += angle
                offset = offset.getXY()
                
                return (self.ships[0].rect.center[0] + offset[0], self.ships[0].rect.center[1] + offset[1])
                
    def is_leader(self, ship):
        if self.ships and ship in self.ships and self.ships.index(ship) == 0:
            return True
        return False
        
        