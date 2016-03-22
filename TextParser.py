'''
Created on 2016-03-18

@author: apovill
'''

import os
import fnmatch
import re


class MetaTool(object):
    '''
    classdocs
    '''

     
    def metaDataLink(self, names, meta):        
        ans = []
        for name in names:
            for elem in meta:
                if name in elem:
                    ans.append(elem)
        return ans
        
    

    def checkNotRed(self, filenames):
        if any('.r3d' in check for check in filenames):
            return 0
        return 1
    
    def alexaMetaExtract(self, filepaths):
        alexa_pattern = '*.ale'
        try:
            metapath = fnmatch.filter(filepaths, alexa_pattern)[0]
        except IndexError:
            print "No metadata file found."
            return None
        with open(metapath, 'r') as f:
            metafile = [x.strip().split('\t') for x in f]
        f.close()
        return metafile
    
    def redMetaExtract(self): 
        print 'Red'
        return 1
    
    def findMetaArgs(self, meta):
        args = []
        for set in meta:
            if "Name" in set:
                for terms in set:
                    args.append(terms)
        return args
    
   
class TextTool(object):
    
    def stripPaths(self, paths):
        res = []
        for anyname in paths:
            res.append(os.path.basename(anyname))
            
        result = self.clipNameSanitize(res)
        return result
    
    def clipNameSanitize(self, names):
        ans = []
        for i in names:
            ans.append(names[names.index(i)].split('.')[0])
        return ans
    
    def notValidCard(self, name):
        patt=re.compile("[A-Z][0-9][0-9][0-9]")
        if re.match(patt, name) is None:
            print "No card was found at the location."
            return 1
        return 0
    
class FileTool(object): 
    
              
    def findFilePaths(self, loc):
        matches = []
        for root, dirnames, filenames in os.walk(loc):
            for files in filenames:
                matches.append(os.path.join(root,files))
                
        return matches