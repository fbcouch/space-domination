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
    
    
def parse(text, width, font):
    '''
    break up a block of text into lines
    '''
    returnVal = []
    start = 0
    end = 0
    while(start < len(text)):
        prev = 0
        while(end >= 0 and end < len(text) and font.size(text[start:end+1])[0] < width):
            prev = end
            end = end+1
            nextSpace = text[end:].find(" ")
            if nextSpace == -1:
                end = len(text)
                if start == prev and not (font.size(text[start:])[0] < width):
                    #special case - we have a really long word at the end
                    end = start
                    while(end >= 0 and end < len(text) and font.size(text[start:end+1])[0] < width):
                        end += 1
            else:
                
                end += nextSpace
                if prev == start and not font.size(text[start:end])[0] < width:
                    end = start
                    while(end >= 0 and end < len(text) and font.size(text[start:end+1])[0] < width):
                        end += 1
                
        
        if end >= 0:    
            if font.size(text[start:end])[0] < width:
                returnVal.append(text[start:end].strip())
                start = end
            else:
                returnVal.append(text[start:prev].strip())
                start = prev
        else:
            returnVal.append(text[start:])
            start = len(text)
    return returnVal

def parse_pointlist(pointlist):
    returnval = []
    i = 0
    while i < len(pointlist):
        f = pointlist.find(";", i)
        if f == -1:
            f = len(pointlist)
        # the next point is defined by [i:f]
        point = pointlist[i:f]
        c = point.find(",")
        if c >= 1: 
            # we have a valid point, grab everything before c as the "x" value and after as "y"
            returnval.append((int(point[:c]),int(point[c+1:])))
        i = f + 1
    return returnval

'''
Asset manager type stuff
'''
assets = {}

def load_common_assets():
    
    assets['explosion1.png'] = load_sprite_sheet('explosion1.png', 100, 100, colorkey = -1)
    assets['explosion3.png'] = load_sprite_sheet('explosion3.png', 100, 100, colorkey = -1)
    assets['shield_hit.png'] = load_sprite_sheet('shield_hit.png', 100, 100, colorkey = -1)
    
    
def get_asset(name):
    if name in assets:
        return assets[name]
    else:
        return None
    