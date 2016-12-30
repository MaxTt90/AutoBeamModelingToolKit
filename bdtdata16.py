# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 19:12:13 2016

@author: cnshayit

Class BDT data 

"""

import os


class BdtData16(object):
    def __init__(self, filePath):
        self.path = filePath
        self.propertyKeys = ['PARTICLE-TYPE', 'NOMINAL-ENERGY', 'PRIMARY-PHOTONS', 'PRIMARY-SIGMA', 'SCATTER-DIST',
                             'SCATTER-SIGMA', 'NORM-VALUE',
                             'GY/MU-DMAX', 'ENERGY-MIN', 'ENERGY-MAX', 'B-VALUE', 'CHARGED-PARTICLES', 'CHARGED-DIST',
                             'CHARGED-RADIUS',
                             'CHARGED-E-MEAN', 'CHARGED-E-MAX', 'PRIMARY-HORN0', 'PRIMARY-HORN1', 'PRIMARY-HORN2',
                             'PRIMARY-HORN3',
                             'PRIMARY-HORN4', 'BIN1-START', 'BIN1-WEIGHT', 'BIN-SEC-WEIGHT', 'SEC-B-VALUE',
                             'SEC-DELTA-B', 'A-VALUE',
                             'Z-VALUE', 'DELTA-B-OAS', 'BRIM-SCATTER-SIGMA', 'MAX-FIELD-RADIUS', 'EFLUENCE-SLOPE',
                             'OAS-UNIT', 'COMMONSCOREPLANE',
                             'CHARGED-FOCUS']
        self.propertyDict = dict.fromkeys(self.propertyKeys, None)

        try:
            self.parseContents()
        except Exception as ex:
            print(ex)

    def getFilePath(self):
        return self.path

    def parseContents(self):
        if not os.path.isfile(self.path):
            return False
        with open(self.path, 'r') as bdtFile:
            while True:
                line = bdtFile.readline()
                if not line:
                    break
                if self._isOasProfile(line):
                    self._parseOasProfile(line)
                else:
                    self._parseContent(line)

        return True

    def _parseContent(self, line):
        tokens = line.strip().split(':')
        if len(tokens) < 2:
            return

        propertyKey = tokens[0].strip()
        propertyVal = tokens[1].strip()

        if propertyKey in self.propertyDict:
            self.propertyDict[propertyKey] = propertyVal

    def _isOasProfile(self, line):
        return str.strip(line).startswith('OAS-PROFILE:')

    def _parseOasProfile(self, line):
        tokens = line.strip().split(':')
        if len(tokens) < 1:
            return

        values = tokens[1].split(' ')
        self.oasProfile = [float(vl) for vl in values if vl]

# def _isVerison(self, line):
#        return str.strip().startswith('BASE-DATA-FILE-VERSION:')
#        
#    def _isBdt16(self, line):
#        tokens = line.strip().split(':')
#        if len(tokens) < 1:
#            return False
#        else:
#            return tokens[1].strip() == '1.6'
