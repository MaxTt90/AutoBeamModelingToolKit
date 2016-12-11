# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:37:27 2016

@author: cnshayit

Class Measurement Analysis Toolkit
"""

class MeasurementAnalysisToolkit(object):
    
    def extractPddPercentages(pddMeasuredData):
        D5 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 5)   
        D10 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 10)
        D20 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 20) 
        
        maxValCor = MeasurementAnalysisToolkit.findMaxValueCoordinate(pddMeasuredData)
        Dmax = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, maxValCor)
        
        return {'DmaxDepth': maxValCor, 'D5Per': D5/Dmax, 'D10Per': D10/Dmax, 'D20Per': D20/Dmax}
    
    def getProfileShift(profileMeasuredData): 
        ''' To be tested '''
        dataPoints = profileMeasuredData.dataPoints
        
        halfVal = 0.5 * max([dp[1] for dp in dataPoints])
        couplePos = []
        for i in range(len(dataPoints) - 2):
            former = dataPoints[i]
            later = dataPoints[i+1]
            
            product = (former[1] - halfVal) * (later[1] - halfVal)
            if(product < 0):
                couplePos.append((former[0] + later[0])/2)
            elif (product == 0):
                pos = (former[0] if former[1] == halfVal else later[0])
                couplePos.append(pos)
            else:
                continue
        
        return couplePos
    
        
    def findMaxValueCoordinate(measuredData):
        dataPoints = measuredData.dataPoints
        
        maxVal = max([dp[1] for dp in dataPoints])
        for dp in dataPoints:
            if dp[1] == maxVal:
                return dp[0]
                      
    def getPointValueFromProfile(measuredData, coordinate):
        dataPoints = measuredData.dataPoints
        
        matched = MeasurementAnalysisToolkit.findMatchedValueOrTheNearest(dataPoints, coordinate)
        if matched is None:
            return None
        elif type(matched) is list:
            return matched[1]
        else:
            return MeasurementAnalysisToolkit.getInterpolatedValue(matched[0], matched[1], coordinate)
            
        
    def getInterpolatedValue(lessNearestPoint, greaterNearestPoint, coordinate):
        k = (lessNearestPoint[1] - greaterNearestPoint[1]) / (lessNearestPoint[0] - greaterNearestPoint[0])
        b = greaterNearestPoint[1] - (k * greaterNearestPoint[0])
        
        return k * coordinate + b
        
        
    def findMatchedValueOrTheNearest(orderedPointList, coordinate):                   
        lessNearestPoint, greaterNearestPoint = None, None
        for point in orderedPointList:
            if point[0] < coordinate:
                lessNearestPoint = point
            elif point[0] == coordinate:    
                return point
            else:
                greaterNearestPoint = point
                break
        
        if lessNearestPoint is not None and greaterNearestPoint is not None:
            return (lessNearestPoint, greaterNearestPoint)
        else:
            return None
        
                    