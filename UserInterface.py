'''
Created on 2016-03-17

@author: apovill
'''

import os
import readline
import pickle

from LogFileCompiler import LogGenerator



class UI(object):
    '''
    This class holds a LogGenerator object which has a path and name, created on construction of a UI class.  It handles all top level
    user domain functions
    '''
    
#    Constructor checks if project is new, if so, creates a valid loggenerator object and log at the path, else loads an old project
#    that the user selects
 
    def __init__(self):
        self.execdir = os.getcwd()
        self.COMMANDS = ["Add Card", "Display Clip Meta", "Quit"]
        os.system('clear')
        if self.newProject():
            self.logname = self.getLogName()
            while self.checkNameSanity(self.logname) is False:
                self.logname = self.getLogName()
            self.logpath = self.getLogLoc()
            while self.checkValidPath(self.logpath) is False:
                self.logpath = self.getLogLoc()
            self.loggen = LogGenerator(self.logpath, self.logname)
            self.loggen.logFileGen()
        else:
            self.loggen = self.loadProject()
            self.logloc = self.loggen.getPath()
            self.logname = self.loggen.getLogsName()

    def newProject(self):
        print "Is this a new project? (y/n): "
        aff = ['yes', 'Yes', 'y', 'YES']
        neg = ['no', 'No', 'NO', 'n']
        ans = raw_input()
        while ans not in neg and ans not in aff:
            print "Please enter a yes or no\nIs this a new Project? (y/n): "
            ans = raw_input()
        if ans in aff:
            return True
        return False
    
    #    Check that the OS can access the path provided.
    def checkValidPath(self, path):
        try:
            os.chdir(path)
        except:
            print "Please enter a valid path."
            return False
        else:
            os.chdir(self.execdir)
            return True
        
    #    Check the OS can write a file with the filename provided.
    def checkNameSanity(self, name):
        os.chdir(self.execdir)
        try:
            with open('name', 'w') as f:
                pass
            os.remove('name')
        except:
            print "Please enter a valid filename"
            return False
        else:
            return True
        
    #    Load an old project
    def loadProject(self):
        os.chdir(self.execdir)
        filename = self.loadDatabase()
        with open('../db/'+filename, 'r') as f:
            data = pickle.load(f)
        f.close()
        return data    
    
    #    Call the loggenerator to add a card to the log
    def addACard(self):
        cardloc = self.getCardLoc()
        self.loggen.addCard(cardloc)
        self.save()
    
    
    def callDirInput(self):
        os.chdir('/')
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        userinput = raw_input('')
        if userinput[:1] is '/':
            return userinput
        return '/'+userinput
        
    def callFileFind(self):
        os.chdir('/')
        return self.readlineCompleteRead()
    
    def loadDatabase(self):
        print "Select Log:"
        for term in os.listdir('../db'):
            print term
        os.chdir('../db')
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        userinput = raw_input('Selection: ')
        os.chdir(self.execdir)
        return userinput
    
    def readlineCompleteRead(self):
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        return raw_input()
    
    
    def menu(self):
        print '\n\n'
        answer = self.menuCall()
        if answer in ['Add Card', 'Add card', 'add card', '1']:
            self.addACard()
            self.menu()
        else:
            if answer in ['Display Clip Meta', '2']:
                self.displayClipMeta()
                self.menu()
            else:
                if answer in ['Quit', 'quit', 'q', '3']:
                    self.quit()
            
            
    def menuCall(self):
        print "Options are:"
        i=1
        for term in self.COMMANDS: 
            print '{0}) {1}'.format(i,term)
            i+=1
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        test = raw_input('Enter section: ')
        if test in self.COMMANDS or test in ['1','2','3']:
            readline.set_completer()
            return test
        else:
            print "Not a valid option, please enter a valid option."
            return self.menuCall()
        
    def displayClipMeta(self):
        selcard = self.getTargetCard()
        selclip = self.getAClip(selcard)
        selclipmeta = selclip.getMeta()
        print selclipmeta
        print len(selclipmeta)
        selclipmetaargs = selcard.getMetaArgs()
        print selclipmetaargs
        print len(selclipmetaargs)
        for terms in selclipmetaargs:
            if len(selclipmeta[selclipmetaargs.index(terms)]) > 50:
                print "{0:30}  ---  {1:50}".format(terms,selclipmeta[selclipmetaargs.index(terms)][:50]+'...')
            else:
                print "{0:30}  ---  {1:50}".format(terms, selclipmeta[selclipmetaargs.index(terms)])
                
    
    def getTargetCard(self):
        currolls = []
        selection = raw_input("Enter Roll (eg. A001): ")
        for card in self.loggen.getCards():
            currolls.append(card.getRoll())
            if selection in currolls:
                return card
        print  "\nNo roll of that name found.  Try again.\n"
        return self.getRoll()
        
    
    def getAClip(self, card):
        selection = raw_input("Enter clip number (eg. 1): ")
        try:
            return card.getClip(int(selection))
        except IndexError:
            print "Clip number does not exist on this card"
            return self.getAClip(card)
        except:
            print "Please enter a number"
            return self.getAClip(card)
    
    def complete(self, text, state):

        for cmd in self.COMMANDS:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1

    
    def getCardLoc(self):
        print 'Enter card location: '
        return self.callDirInput()
        
    
    def getLogLoc(self):
        print 'Enter path for logfile: '
        return self.callDirInput()
    
    def getLogName(self):
        print 'What is your project name: '
        return raw_input()
    
    def getLogPath(self):
        print 'Select Logfile: '
        return self.callFileFind()
    
    def save(self):
        os.chdir(self.execdir)
        if not os.path.exists('../db/'):
            os.mkdir('../db/')
        with open('../db/'+self.logname, 'w') as f:
            pickle.dump(self.loggen, f)
        f.close()
        print "Current session saved"
        
    def quit(self):
        print "Do you want to save now? (y/n)"
        aff = ['yes', 'Yes', 'y', 'YES']
        neg = ['no', 'No', 'NO', 'n']
        ans = raw_input()
        while ans not in neg and ans not in aff:
            print "Please enter a yes or no\nDo you want to save now? (y/n): "
            ans = raw_input()
        if ans in aff:
            self.save()
        else:
            pass