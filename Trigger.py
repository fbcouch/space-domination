'''
Created on Jul 13, 2012

@author: jami
'''
from PopupMessage import PopupMessage
import Utils

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
                count = 0
                for ship in context.shipSpriteGroup:
                    if ship.tag.count(self.tag) > 0:
                        count += 1
                if count == 0: self.completed = True
                else:
                    self.display_text = self.orig_display_text + " (" + str(count) + " remain)"
    
        if not completed and self.completed and context:
            if self.message_title and self.message_body:
                # display a message
                context.messageList.append(PopupMessage(self.message_title, self.message_body, 600, self.message_icon_image))

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