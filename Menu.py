'''
Created on Jun 13, 2012

@author: Jami
'''
from pygame.locals import *
from simplemenuclass.menu import cMenu, EVENT_CHANGE_STATE
import math
import os
import pygame
import random
import sys

MENU_MAIN = 0 # 0-99 reserved for menu pages
MENU_OPTIONS = 1
MENU_EXIT = 100 # 100-199 reserved for actions
MENU_RESUME = 101
MENU_MISSION = 200 # missions will start with 2xx with xx being mission ID

    
class MenuManager(object):
    menuList = None
    selectedMenu = 0 # default to no menu shown
    
    def __init__(self, screen = None):
        self.menuList = []
        # menu 0 = main menu
        self.menuList.append(cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                                [('Resume', MENU_RESUME, None),
                                 ('Options', MENU_OPTIONS, None),
                                 ('Exit', MENU_EXIT, None)]))
        
        
        # menu 1 = options menu
        self.menuList.append(cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                                   [('Back', MENU_MAIN, None)]))
        
        return
    
    def draw(self):
        self.menuList[self.selectedMenu].redraw_all()
        self.menuList[self.selectedMenu].draw_buttons()
    
    def update(self, event = None):
        rect_list, state = self.menuList[self.selectedMenu].update(event, self.selectedMenu)    
        if state != self.selectedMenu: self.menu_state_parse(state)
        
    
    def menu_state_parse(self, state = 0):
        if(state == MENU_MAIN):
            self.selectedMenu = MENU_MAIN
        elif(state == MENU_RESUME):
            self.selectedMenu = -1
        elif(state == MENU_EXIT):
            sys.exit(0)
        elif(state == MENU_OPTIONS):
            self.selectedMenu = MENU_OPTIONS
        
        self.menuList[self.selectedMenu].set_alignment('center', 'center')
        self.menuList[self.selectedMenu].set_center(True, True)  
        self.menuList[self.selectedMenu].update(pygame.event.Event(EVENT_CHANGE_STATE, key = 0), self.selectedMenu)
        
        
        return self.selectedMenu
    
    def is_active(self):
        if self.selectedMenu >= 0 and self.selectedMenu < len(self.menuList):
            return True
        else:
            return False