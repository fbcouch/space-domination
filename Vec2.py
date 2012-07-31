'''
Created on Jun 24, 2012

@author: Jami
'''
import math
class Vec2(object):
    magnitude = 0
    theta = 0
    
    def __init__(self, mag, t):
        self.magnitude = mag
        self.theta = t
    
    def add(self, pVec = None):
        if pVec is None: return self
        #if not pVec is Vec2: return self
        
        v1 = self.getXY()
        v2 = pVec.getXY()
        
        v3 = v1[0] + v2[0], v1[1] + v2[1]
        
        self.setXY(v3[0],v3[1])
        
        return self
        
    def getXY(self):
        return (self.magnitude * math.cos(math.radians(self.theta))), (-1 * self.magnitude * math.sin(math.radians(self.theta)))
    
    def setXY(self, x = 0.0, y = 0.0):
        mag = 0.0
        t = 0.0
        
        mag = math.sqrt(x*x + y*y)
        if mag == 0:
            self.magnitude = 0
            self.theta = 0
            return self
        
        if y == 0:
            t = math.degrees(math.acos(float(x) / float(mag)))
        elif x == 0:
            t = math.degrees(math.asin(float(- y) / float(mag)))
            
        else:
            t = math.degrees(math.atan(float(- y) / float(x)))
            if x < 0:
                t += 180
            
        self.magnitude = mag
        self.theta = (t + 360) % 360
        return self