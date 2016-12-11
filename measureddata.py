# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:34:16 2016

@author: cnshayit

Class for measured data

"""

import os
import re

class MeasuredData(object):
    
    def __init__(self, path):
        self.path = path
        
        try:
            self.parseContents()
        except Exception as ex:
            print(ex)
    
    def parseContents(self):
        if not os.path.isfile(self.path):
            return False
        
        if not self._parseName():
            return False
        
        self._parseDataPoints()
        return True        
        
    def _parseDataPoints(self):
        self.dataPoints = []
        with open(self.path, 'r') as measuredFile:
            while True:
                line = measuredFile.readline()
                if not line:
                    break
                
                tokens = line.strip().split(' ')
                self.dataPoints.append([float(tokens[0]), float(tokens[-1])])
                           
    def _parseName(self):
        name = os.path.basename(self.path)
        self.name = name
        
        namepat = re.compile(r"(AB|GT|Z|DGBTA)(_)(\d+mv)(\d+.\d+x\d+.\d+)(.\d+)")
        tokens = namepat.match(self.name).group(1, 2, 3, 4, 5)
        if len(tokens) < 1:
            return False
        
        self.orientationType = tokens[0].strip()
        self.energy = float(tokens[2][:2])
        self.fieldSize = [float(tk) for tk in tokens[3].split('x')]
        self.depth = float(tokens[4][1:])
        return True
        