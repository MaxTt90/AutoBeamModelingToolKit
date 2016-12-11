# -*- coding: utf-8 -*-
"""Class for ptw data
"""
import os
import sys

from ptwscan import PtwScan

class PtwData(object):

    def __init__(self, path):
        self.path = path
        self.scans = []
        self.propertyKeys = ['FORMAT', 'FILE_CREATION_DATE', 'LAST_MODIFIED', 'END_SCAN_DATA']
        self.propertyDict = dict.fromkeys(self.propertyKeys, None)
        
        try:
            self.parseFileContent()
        except Exception as ex:
            sys.stdout(ex)

    def getPath(self):
        return self.path
    
    def parseFileContent(self):
        if not os.path.isfile(self.path):
            return False
    
        foundContents = False    
        with open(self.path, 'r') as ptwFile:
            while not foundContents:
                line = ptwFile.readline()
                if not line:
                    break
                
                if not self._isComment(line) and not self._isStartFile(line):
                    break
                
                foundContents = True
                self._parseContents(ptwFile)
        if not foundContents:
            sys.stdout("File is not a PTW MEPHYSTO mc^2 file.")
            return False       
        return True
    
    def _parseContents(self, ptwFile): 
        while True:
            line = ptwFile.readline()
            if not self._isComment(line):
                if self._isStartScan(line):
                    scan = PtwScan(ptwFile)
                    self.scans.append(scan)
                elif self._isEndFile(line):
                    return
                else:
                    self._parseContent(line)
                    
    def _isComment(self, line):
        return str.strip(line).startswith('\'')        
        
    def _isStartFile(self, line):
        return str.strip(line).startswith('BEGIN_SCAN_DATA')   
        
    def _isEndFile(self, line):
        return str.strip(line).startswith('END_SCAN_DATA')
        
    def _isStartScan(self, line):
        return str.strip(line).startswith('BEGIN_SCAN') 
        
    def _parseContent(self, line):
        tokens = line.split('=', 2)
        if len(tokens) < 1:
            return
        
        propertyKey = tokens[0].strip()
        propertyVal = tokens[1].strip()

        if propertyKey in self.propertyDict:
            self.propertyDict[propertyKey] = propertyVal  
                        
                    
        

        
    