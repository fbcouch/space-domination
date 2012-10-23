'''
Created on Jul 13, 2012

@author: jami
'''
from PopupMessage import PopupMessage
import Utils
import consts

class Trigger(object):
    '''
    XML Object:
        <trigger
            id - integer identifier for the trigger (should be unique)
            type - (primary-objective, secondary-objective)
            condition - (destroy-attached, destroy-class, survive-attached, survive-class, mission-start)
            parent - (target for "attached" conditions)
            tag - used for grouping
            display-text - basis for objective display in HUD
            message-icon-file - usually an avatar for the "speaker" of a message   |
            message-title - the title of a message (often the "speaker"'s name)    | messages are displayed upon meeting the "condition"
            message-body - the contents of a message                               |
            
            attrs - unused at present
        />
    '''
    id = 0
    type = ""
    condition = ""
    attrs = None
    tag = ""
    display_text = ""
    message_icon_file = ""
    message_title = ""
    message_body = ""
    
    message_icon_image = None
    
    parent = None
    
    completed = False
    
    spawn_list = None
    
    def __init__(self):
        '''
        Constructor
        '''
        attrs = []
        
    def update(self, context = None):
        completed = self.completed
        
        if self.condition.count("destroy-attached") > 0:
            if not self.parent or self.parent.health <= 0:
                self.completed = True
        
        if self.condition.count("mission-start") > 0:
            if not self.completed:
                self.completed = True
                
        if self.condition == "destroy-class":
            if context:
                count = len(self.get_attached(context.shipSpriteGroup))
                if count == 0: 
                    self.completed = True
                    self.display_text = self.orig_display_text
                else:
                    self.display_text = self.orig_display_text + " (" + str(count) + " remain)"
        
        if self.condition == "survive-attached":
            if not self.parent or self.parent.health <= 0:
                self.completed = False
            else:
                self.completed = True
                
        if self.condition == "survive-class":
            if context:
                count = len(self.get_attached(context.shipSpriteGroup))
                if count == 0:
                    self.completed = False
                    self.display_text = self.orig_display_text
                else:
                    self.display_text = self.orig_display_text + " (" + str(count) + " remain)"
                    self.completed = True
        
        if self.condition == "spawn-at-time":
            if context and not self.completed and not self.spawn_list:
                self.spawn_list = self.get_attached(context.shipSpriteGroup)
            
                for sp in self.spawn_list:
                    sp.active = False
                    
            
            if context and self.attrs and len(self.attrs) > 0:
                end_at = self.attrs[0].split(":")
                end_at = float(end_at[0]) * consts.TIME_MIN_MUL + float(end_at[1]) * consts.TIME_SEC_MUL
                if context.elapsedTime >= end_at:
                    self.completed = True
                    self.display_text = self.orig_display_text
                    for sp in self.spawn_list:
                        sp.active = True
                        self.spawn_list.remove(sp)
                    
                else:
                    self.completed = False
                    dt = end_at - context.elapsedTime
                    m = int(dt / consts.TIME_MIN_MUL)
                    dt -= m * consts.TIME_MIN_MUL
                    s = int(dt / consts.TIME_SEC_MUL)
                    if s < 10:
                        text = " (%i:0%i until spawn)" % (m, s)
                    else:
                        text = " (%i:%i until spawn)" % (m, s)
                    self.display_text = self.orig_display_text + text
        
        if self.condition == "spawn-on-destroy":
            if context and not self.completed and not self.spawn_list:
                self.spawn_list = self.get_attached(context.shipSpriteGroup)
                for sp in self.spawn_list:
                    sp.active = False
                    
            if context and not self.completed:
                if self.attrs and len(self.attrs) > 0:
                    count = 0
                    for ship in context.shipSpriteGroup:
                        if ship.tag.count(self.attrs[0]) > 0:
                            count += 1
                    if count > 0:
                        self.completed = False
                    else:
                        self.completed = True
                        for sp in self.spawn_list:
                            sp.active = True
                            self.spawn_list.remove(sp)

                else:
                    self.completed = True
                    for sp in self.spawn_list:
                        sp.active = True
                        self.spawn_list.remove(sp)
        
        if self.condition == "lose-at-time":
            if context and self.attrs and len(self.attrs) > 0:
                end_at = self.attrs[0].split(":")
                end_at = float(end_at[0]) * consts.TIME_MIN_MUL + float(end_at[1]) * consts.TIME_SEC_MUL
                if context.elapsedTime >= end_at:
                    self.completed = False
                    self.display_text = self.orig_display_text
                    if context.gameState != context.GAMESTATE_GAMEOVER: context.endMission()
                else:
                    self.completed = True
                    completed = True
                    dt = end_at - context.elapsedTime
                    m = int(dt / consts.TIME_MIN_MUL)
                    dt -= m * consts.TIME_MIN_MUL
                    s = int(dt / consts.TIME_SEC_MUL)
                    if s < 10:
                        text = " (%i:0%i remains)" % (m, s)
                    else:
                        text = " (%i:%i remains)" % (m, s)
                    self.display_text = self.orig_display_text + text
                    
        if self.condition == "win-at-time":
            if context and self.attrs and len(self.attrs) > 0:
                end_at = self.attrs[0].split(":")
                end_at = float(end_at[0]) * consts.TIME_MIN_MUL + float(end_at[1]) * consts.TIME_SEC_MUL
                if context.elapsedTime >= end_at:
                    self.completed = True
                    self.display_text = self.orig_display_text
                    if context.gameState != context.GAMESTATE_GAMEOVER: context.endMission()
                else:
                    self.completed = False
                    completed = False
                    dt = end_at - context.elapsedTime
                    m = int(dt / consts.TIME_MIN_MUL)
                    dt -= m * consts.TIME_MIN_MUL
                    s = int(dt / consts.TIME_SEC_MUL)
                    if s < 10:
                        text = " (%i:0%i remains)" % (m, s)
                    else:
                        text = " (%i:%i remains)" % (m, s)
                    self.display_text = self.orig_display_text + text
            
    
        if not completed == self.completed and context:
            if self.message_title and self.message_body:
                # display a message
                context.messageList.append(PopupMessage(self.message_title, self.message_body, PopupMessage.DEFAULT_DURATION, context.screen.get_width(), self.message_icon_image))
                
                
    def get_attached(self, shiplist):
        '''get a list of the attached ships'''
        attached = []
        if self.condition.count("class") > 0 or self.condition.count("spawn") > 0:
            for ship in shiplist:
                if ship.tag.count(self.tag) > 0:
                    attached.append(ship)
        elif self.parent:
            attached.append(self.parent)
        return attached

    def toXML(self):
        return "<trigger />"
        
def CreateTrigger(id, type = "", condition = "", attrs = "", tag = "", display_text = "", message_icon_file = "", message_title = "", message_body = ""):
    tg = Trigger()
    tg.id = id
    tg.type = type
    tg.condition = condition
    tg.display_text = display_text
    tg.orig_display_text = display_text
    tg.message_icon_file = message_icon_file
    tg.message_title = message_title
    tg.message_body = message_body
    tg.tag = tag
    
    # parse attrs
    tg.attrs = attrs.split(",")
    
    # load image
    if tg.message_icon_file:
        try:
            tg.message_icon_image, rect = Utils.load_image(tg.message_icon_file)
        except SystemExit, message:
            print "Error loading image: " + message_icon_file
    
    return tg