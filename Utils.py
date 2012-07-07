'''
Created on Apr 29, 2012

@author: Jami
'''

import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('assets', os.path.join('gfx', name))
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('assets', os.path.join('sfx', name))
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound

def load_sprite_sheet(name, width, height, colorkey = None):
    fullimage, fullrect = load_image(name, colorkey)
    spriteImages = []
    cols = int(fullrect.width / width)
    rows = int(fullrect.height / height)
    
    col = 0
    row = 0
    while row < rows:
        col = 0
        while col < cols:
            #image = pygame.Surface((width, height))
            #image = image.convert()
            #image.blit(fullimage, (0, 0), pygame.rect.Rect(col * width, row * height, width, height))
            image = fullimage.subsurface(pygame.rect.Rect(col * width, row * height, width, height))
            #image = image.convert_alpha()
            spriteImages.append(image)
            col += 1
        row += 1
    
    return spriteImages
    
    
    
    
