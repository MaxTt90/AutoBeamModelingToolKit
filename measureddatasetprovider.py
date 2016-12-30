# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 10:26:55 2016

@author: cnshayit

Class MeasuredDataSetProvider
"""

import os
from measureddata import MeasuredData


class MeasuredDataSetProvider(object):
    def __init__(self, dirPath, rex):
        self.path = dirPath
        self.rex = rex

    def getDirPath(self):
        return self.path

    def getAllMeasuredDataInDir(self):
        names = os.listdir(self.path)

        validpaths = [os.path.join(self.path, name) for name in names if self.rex.match(name)]
        if len(validpaths) < 1:
            return False

        self.measuredDataSet = [MeasuredData(path) for path in validpaths]
        return True
