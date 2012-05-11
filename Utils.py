'''
Created on Apr 29, 2012

@author: Jami
'''

from panda3d.core import TextNode, Point2, Point3, Vec3, Vec4
from direct.gui.OnscreenText import OnscreenText

SPRITE_POS = 25 #sets the default sprite depth...this should always be 2 and we can move the camera around to zoom.

'''
    This was taken from the Asteroids sample program in Panda3D
'''
def genLabelText(text, i):
    return OnscreenText(text = text, pos = (-1.3, .95-.05*i), fg=(1,1,0,1),
                      align = TextNode.ALeft, scale = .05)

def loadObject(tex = None, pos = Point2(0,0), depth = SPRITE_POS, scale = 1,
               transparency = True, parent = None):
    obj = loader.loadModel("assets/models/plane") #Every object uses the plane model
    if parent: 
        obj.reparentTo(parent)
    obj.setPos(Point3(pos.getX(), depth, pos.getY())) #Set initial position
    obj.setScale(scale)                 #Set initial scale
    obj.setBin("unsorted", 0)           #This tells Panda not to worry about the
                                        #order this is drawn in. (it prevents an
                                        #effect known as z-fighting)
    obj.setDepthTest(False)             #Tells panda not to check if something
                                        #has already drawn in front of it
                                        #(Everything in this game is at the same
                                        #depth anyway)
    if transparency: obj.setTransparency(1) #All of our objects are trasnparent
    if tex:
        tex = loader.loadTexture("assets/"+tex) #Load the texture
        obj.setTexture(tex, 1)                           #Set the texture

    return obj