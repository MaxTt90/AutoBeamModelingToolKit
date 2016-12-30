# -*- coding: utf-8 -*-
"""
Class for PTW data point
"""


class PtwDataPoint:
    
    def __init__(self, position, measurement, referenceMeasurement = None):
        self.position = position
        self.measurement = measurement
        self.referenceMeasurement = referenceMeasurement
        
    def tostring(self):
        return self.position + ', ' + self.measurement + ', ' + self.referenceMeasurement
