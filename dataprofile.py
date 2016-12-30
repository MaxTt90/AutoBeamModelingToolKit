# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 10:15:44 2016

@author: cnshayit
"""


class DataProfile(object):
    def __init__(self, orientationType, energy, fieldSize, depth, ssd=90):
        self.orientationType = orientationType
        self.energy = energy
        self.fieldSize = fieldSize
        self.depth = depth
        self.ssd = ssd

    def setDataPoints(self, rawDataPoints):
        # Coordinate system transform ignored.
        self.dataPoints = rawDataPoints

    def setWedgeAngle(self, wedgeAngle):
        self.wedgeAngle = wedgeAngle

    def setCollimatorAngle(self, collimatorAngle):
        self.collimatorAngle = collimatorAngle

    def setSsd(self, ssd):
        self.ssd = ssd

    def setGantryAngle(self, gantryAngle):
        self.gantryAngle = gantryAngle
