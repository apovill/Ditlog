'''
Created on 2016-03-17

This module is intended to store all of the relevant video information.  It
houses 'clip' classes, which are names and metadata, as well as 'card' 
classes, which house the clips.

The 'card' must fill itself with clips when it is created by "LogParser",
which accepts a "card" and outputs a "log" with values from "clips" in the
"card".

@author: apovill
'''

class Card(object):
    '''
    A "Card" is a collection of "clips", it's the basic building block
    of the log to be output by MyDitLog.  
    '''
    def __init__(self, cardnm, clips, meta):
        '''
        Constructor
        '''
        self.cardname = cardnm
        self.clips = clips
        self.metaargs = meta
        
    def getClip(self, anint):
        return self.clips[anint-1]
    
    def getNumClips(self):
        return len(self.clips)
    
    def getClips(self):
        return self.clips
    
    def getMetaArgs(self):
        return self.metaargs
    
    def getCardName(self):
        return self.cardname
    
    def getClipNames(self):
        clipnames = []
        for aclip in self.clips:
            clipnames.append(aclip.getClipName())
        return clipnames
    
    def getCamera(self):
        return self.cardname[:1]
    
    def getRoll(self):
        return self.cardname[:4]
    
class Clip(object):    
    '''
    A 'clip' is a file that has a 'name' and associated metadata.
    '''
    
    def __init__(self, name, meta):
        self.name=name
        self.meta=meta
        
        
    def getClipName(self):
        return self.name
    
    def getMeta(self):
        return self.meta

