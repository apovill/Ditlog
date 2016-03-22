'''
Created on 2016-03-19

@author: apovill
'''

import os

from ClipInfo import Card, Clip
from TextParser import MetaTool, TextTool, FileTool


class LogGenerator(object):
    '''
    classdocs
    '''
    __name__ = 'LogGenerator'
#    __module__ = os.path.splitext(os.path.basename(__file__))[0]

    def __init__(self, path, name):
        '''
        Constructor
        '''
        self.ftool = FileTool()
        self.logpath = path
        self.logname = name
        self.logmetaargs = ""
        self.cards = []
        self.cameras = []

        
    def getLogsName(self):
        return self.logname
    
    def getPath(self):
        return self.logpath
    
    def setLogName(self, newname):
        self.logname = newname
        
    def logFileGen(self):
        f = open(self.logpath+self.logname, 'w+')
        self.defaultLog(f)
        f.close()
        
    def defaultLog(self, myfile):
        sf = open('default.txt')
        default = sf.readlines()
        sf.close()        
        for terms in default:
            myfile.write(terms)

    def getCards(self):
        return self.cards
    
    
    def addCard(self, cardloc):
        load = CardLoader()
        cardname = os.path.basename(os.path.normpath(cardloc))
        clippaths = self.ftool.findFilePaths(cardloc)
        card = load.loadCard(cardname, clippaths)
        if card is None:
            print "No card was added to log"
        else:
            self.cards.append(card)
            print len(self.cards)
            if len(self.cards)==1:
                self.writeFirstRoll(card)
                self.writeNewCamera(card)
                self.cameras.append(card.getCamera())
            else:
                self.writeRoll(card)
                if self.newCamera(card):
                    self.writeNewCamera(card)
                    self.cameras.append(card.getCamera())
                else:
                    self.appendClipNames(card)
            
    def newCamera(self, card):
        if len(self.cameras) == 0:
            return True
        else:
            if card.getCamera() not in self.cameras:
                return True
            else:
                return False

        
    def writeNewCamera(self, card):
        cam = card.getCamera()
        
        template = '{0} Cam:\n------\n\nClip\t\t\tRoll\tCard\tScene\t\tTake\tNotes\n\n'.format(cam)
        with open(self.logpath+self.logname, 'a') as f:
            f.write(template)
        f.close()
        self.writeClipNames(card)
        
    def writeFirstRoll(self, card):
        
        curlines = []
        print card.getRoll()
        with open(self.logpath+self.logname, 'r+') as f:
            
            for line in f:
                curlines.append(line)
                if  'Completed' in line and len(self.cards)==1:
                    curlines.append('\n'+card.getRoll())
            f.seek(0,0)
            for line in curlines:
                f.write(line)
                
    def writeRoll(self, card):
        
        lastwrittencard = self.cards[len(self.cards)-2]
        lastwrittenroll = lastwrittencard.getRoll()

        curlines = []
        
        with open(self.logpath+self.logname, 'r+') as f:
            for line in f:
                curlines.append(line)
                if  line == lastwrittenroll+'\n':
                    curlines.append(card.getRoll()+'\n')
            f.seek(0,0)
            for line in curlines:
                f.write(line)
    
    def writeClipNames(self, card):
        
        with open(self.logpath+self.logname, 'a') as f:
            for names in card.getClipNames():
                if names is card.getClipNames()[0]:
                    f.write(names+'\t'+card.getRoll()+'\t\t\t\t\t\n')
                else:
                    f.write(names+'\t\t\t\t\t\t\n')
            f.write('\n')
        f.close()
    
    def appendClipNames(self, card):
        
        precamcards = []
        for allcard in self.cards:
            if allcard.getCamera() == card.getCamera():
                precamcards.append(allcard)
        lastcardofcam = precamcards[len(precamcards)-2]
        
        lastclip = lastcardofcam.getClip(lastcardofcam.getNumClips())
        
        curlines = []
        
        with open(self.logpath+self.logname, 'r+') as f:
            for line in f:
                curlines.append(line)
                if lastclip.getClipName() in line:
                    curlines.append('\n')
                    for allname in card.getClipNames():
                        if allname is card.getClipNames()[0]:
                            curlines.append(allname+'\t'+card.getRoll()+'\t\t\t\t\t\n')
                        else:
                            curlines.append(allname+'\t\t\t\t\t\t\n')
                    
            f.seek(0,0)
            for line in curlines:
                f.write(line)
        
        
class CardLoader(object):

    
    def __init__(self):
        self.ttool = TextTool()
        self.mtool = MetaTool()
        
    def loadCard(self, cardname, filepaths):
        if self.ttool.notValidCard(cardname):
            return None
        filenames = self.ttool.stripPaths(filepaths)
        clipmeta = self.findMetaData(filepaths)
        if clipmeta is None:
            return None
        orderednames = self.fileMatch(clipmeta, filenames)
        if len(orderednames) == 0:
            print "Video files do not match card metadata"
            return None
        metaargs = self.metaArgs(clipmeta)
        clips = self.clipBuilder(orderednames, clipmeta)
        return Card(cardname, clips, metaargs)
    
    def findMetaData(self, filepaths):
        if self.mtool.checkNotRed(filepaths):
            return self.mtool.alexaMetaExtract(filepaths)
        return self.mtool.redMetaExtract()
    
    def fileMatch(self, meta, filenames):
        ans = []
        for line in meta:
            for filename in filenames:
                if filename in line:
                    ans.append(filename)
        return ans
    
    def metaArgs(self, meta):
        return self.mtool.findMetaArgs(meta)
    
    
    def clipBuilder(self, names, meta):
        cleanmeta = self.mtool.metaDataLink(names, meta)
        card = []
        for clipn in names:
            for metalist in cleanmeta:
                if clipn in metalist:
                    newclip = Clip(clipn, metalist)
                    card.append(newclip)
        return card
