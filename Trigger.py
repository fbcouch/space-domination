'''
Created on Jul 13, 2012

@author: jami
'''
import Utils

class Trigger(object):
    '''
    classdocs
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

    def __init__(self):
        '''
        Constructor
        '''
        attrs = []
        
    def update(self, context = None):
        
        pass
    
    def toXML(self):
        return "<trigger />"
        
def CreateTrigger(id, type = "", condition = "", attrs = "", tag = "", display_text = "", message_icon_file = "", message_title = "", message_body = ""):
    tg = Trigger()
    tg.id = id
    tg.type = type
    tg.condition = condition
    tg.display_text = display_text
    tg.message_icon_file = message_icon_file
    tg.message_title = message_title
    tg.message_body = message_body
    
    # parse attrs
    tg.attrs = attrs.split(",")
    
    # load image
    if tg.message_icon_file:
        try:
            tg.message_icon_image, rect = Utils.load_image(tg.message_icon_file)
        except SystemExit, message:
            print "Error loading image: " + message_icon_file
    
    return tg