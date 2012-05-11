'''
Created on Apr 30, 2012

@author: Jami
'''

from panda3d.core import TextNode, Point2, Point3, Vec3, Vec4, NodePath
import Utils

class Sprite(object):
    '''
    classdocs
    '''
    nodePath = None
    velocity = Vec3(0,0,0)
    accel = Vec3(0,0,0)
    
    def __init__(self, node = None, rotation = 0):
        self.nodePath = node
        if(self.nodePath): self.nodePath.setR(rotation)
        
        
    def getPos(self):
        if(self.nodePath):
            return Point2(self.nodePath.getPos().getX(), self.nodePath.getPos().getZ())
        else:
            return Point2(0,0)
    
    def setPos(self, pos = Point2(0,0)):
        if(self.nodePath):
            self.nodePath.setPos(Point3(pos.getX(), self.nodePath.getPos().getY(), pos.getY()))
            
    
    def getVel(self): return self.velocity
    def setVel(self, vel = Vec3(0,0,0)): self.velocity = vel

    def getAccel(self): return self.accel
    def setAccel(self, accel = Vec3(0,0,0)): self.accel = accel
    
    def getR(self): return self.nodePath.getR()
    def setR(self, r): self.nodePath.setR(r)