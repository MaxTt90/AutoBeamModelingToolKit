# -*- coding: utf-8 -*-
"""
Class for ptw scan
"""
import sys
from ptwdatapoint import PtwDataPoint

class PtwScan(object):
    
    def __init__(self, fileObject):
        self.fileObject = fileObject
        self.propertyKeys = ['TASK_NAME', 'PROGRAM', 'COMMENT', 'MEAS_DATE', 'LINAC', 'MODALITY', 'ISOCENTER', 
                             'INPLANE_AXIS', 'CROSSPLANE_AXIS', 'DEPTH_AXIS', 'INPLANE_AXIS_DIR', 'CROSSPLANE_AXIS_DIR', 
                             'DEPTH_AXIS_DIR', 'ENERGY', 'NOMINAL_DMAX', 'SSD', 'SCD', 'BLOCK', 'WEDGE', 'WEDGE_ANGLE', 
                             'FIELD_INPLANE', 'FIELD_CROSSPLANE', 'FIELD_TYPE', 'GANTRY', 'GANTRY_UPRIGHT_POSITION', 
                             'GANTRY_ROTATION', 'COLL_ANGLE', 'COLL_OFFSET_INPLANE', 'COLL_OFFSET_CROSSPLANE', 
                             'SCAN_DEVICE', 'SCAN_DEVICE_SETUP', 'ELECTROMETER', 'RANGE_FIELD', 'RANGE_REFERENCE', 
                             'DETECTOR', 'DETECTOR_RADIUS', 'DETECTOR_NAME', 'DETECTOR_SN', 'DETECTOR_CALIBRATION', 
                             'DETECTOR_IS_CALIBRATED', 'DETECTOR_REFERENCE', 'DETECTOR_REFERENCE_RADIUS', 'DETECTOR_REFERENCE_NAME', 
                             'DETECTOR_REFERENCE_SN', 'DETECTOR_REFERENCE_IS_CALIBRATED', 'DETECTOR_REFERENCE_CALIBRATION', 
                             'REF_FIELD_DEPTH', 'REF_FIELD_INPLANE', 'REF_FIELD_CROSSPLANE', 'REF_SCAN_POSITIONS', 'SCAN_CURVETYPE', 
                             'SCAN_DEPTH', 'SCAN_OFFAXIS_INPLANE', 'SCAN_OFFAXIS_CROSSPLANE', 'SCAN_ANGLE', 'SCAN_DIAGONAL', 
                             'SCAN_DIRECTION', 'MEAS_MEDIUM', 'MEAS_PRESET', 'MEAS_TIME', 'MEAS_UNIT', 'SCAN_SPEEDS',
                             'DELAY_TIMES', 'PRESSURE', 'TEMPERATURE', 'NORM_TEMPERATURE', 'CORRECTION_FACTOR', 'EXPECTED_MAX_DOSE_RATE', 
                             'END_SCAN ']
        self.propertyDict = dict.fromkeys(self.propertyKeys, None)
        
        try:
            self._parseContents()
        except Exception as ex:  
            sys.stdout(ex)

    def _parseContents(self):
        while True:
            line = self.fileObject.readline()
            if not str.isspace(line) and not self._isComment(line):
                if self._isBeginData(line):
                    self._parseDataPoints(self.fileObject)
                elif self._isEndScan(line):
                    tokens = line.split(' ', 2)
                    tokenswithoutemptystring = [tk for tk in tokens if tk]
                    self.scanNumber = float(tokenswithoutemptystring[1].strip())
                    break
                else:
                    self._parseContent(line)
    
    def _parseContent(self, line):
        tokens = line.split('=', 2)
        if len(tokens) < 1:
            return
        
        propertyKey = tokens[0].strip()
        propertyVal = tokens[1].strip()

        if propertyKey in self.propertyDict:
            self.propertyDict[propertyKey] = propertyVal    
        
    def _parseDataPoints(self, fileObject):
        self.datapoints = []
        while True:
            line = fileObject.readline()
            if self._isEndData(line):
                break
            
            tokens = line.strip().split('\t')
            tokenswithoutemptystring = [tk for tk in tokens if tk]
            if len(tokenswithoutemptystring) > 1:
                position = float(tokenswithoutemptystring[0].strip())
                measurement = float(tokenswithoutemptystring[1].strip())
                if len(tokenswithoutemptystring) > 2:
                    referenceMeasurement = float(tokenswithoutemptystring[2].strip())
                    self.datapoints.append(PtwDataPoint(position, measurement, referenceMeasurement))
                else:
                    self.datapoints.append(PtwDataPoint(position, measurement))
                
    def _isEndData(self, line):
        return str.strip(line).startswith('END_DATA')
    
    def _isBeginData(self, line):
        return str.strip(line).startswith('BEGIN_DATA')
    
    def _isComment(self, line):
        return str.strip(line).startswith('\'')
    
    def _isEndScan(self, line):
        return str.strip(line).startswith('END_SCAN ')