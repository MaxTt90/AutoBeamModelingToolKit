# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:37:27 2016

@author: cnshayit

Class Measurement Analysis Toolkit
"""
import math

class MeasurementAnalysisToolkit(object):
    
    def extractPddPercentages(pddMeasuredData):
        '''Description: Extract pdd percentages
            
            Arguments: Pdd measured data
            
            Return: A dictionary with pdd percentages: {'DmaxDepth', 'D5Per', 'D10per', 'D20Per'}            
        '''
        D5 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 5)   
        D10 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 10)
        D20 = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, 20) 
        
        maxValCor = MeasurementAnalysisToolkit.findMaxValueCoordinate(pddMeasuredData)
        Dmax = MeasurementAnalysisToolkit.getPointValueFromProfile(pddMeasuredData, maxValCor)
        
        return {'DmaxDepth': maxValCor, 'D5Per': D5/Dmax, 'D10Per': D10/Dmax, 'D20Per': D20/Dmax}
    
    def getProfileShift(profileMeasuredData):
        '''Description: Get profile shift
            
            Arguments: Profile measured data
            
            Return: Shift value or None if can't find couple positions.            
        '''
        couplePos = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData)
        if len(couplePos) != 2:
            return None
        else: 
            return 0.5 * (couplePos[0] + couplePos[1])
            
    def getProfileFieldWidth(profileMeasuredData):
        '''Description: Get field width
            
            Arguments: Profile measured data
            
            Return: Field width or None if can't find couple positions.            
        '''
        couplePos = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData)
        if len(couplePos) != 2:
            return None
        else:
            return (couplePos[1] - couplePos[0])
    
    def getProfileWidthError(profileMeasuredData):
        '''Description: Get width error
            
            Arguments: Profile measured data
            
            Return: Width error.            
        '''
        fieldWidth = MeasurementAnalysisToolkit.getProfileFieldWidth(profileMeasuredData)
        fieldSizeX = profileMeasuredData.fieldSize[0] / 10.0 #Unit Transform
        fieldSizeY = profileMeasuredData.fieldSize[1] / 10.0 
        
        if profileMeasuredData.orientationType == 'AB':
            return fieldWidth - fieldSizeX             
        elif profileMeasuredData.orientationType == 'GT':
            return fieldWidth - fieldSizeY
        elif profileMeasuredData.orientationType == 'DGBTA':
            return fieldWidth - math.sqrt(fieldSizeX * fieldSizeX + fieldSizeY * fieldSizeY)
        else:
            raise ValueError('Measured data orientation type should be AB, GT, DGBTA.')
                                          
    def getProfileFlatness(profileMeasuredData):
        '''Description: Get flatness
            
            Arguments: Profile measured data
            
            Return: Flatness or None if can't find couple positions.            
        '''
        couplePos = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData, 0.8)

        if len(couplePos) != 2:
            return None        
        
        dataValsWithinRange = [dp[1] for dp in profileMeasuredData.dataPoints if (dp[0] > couplePos[0] and dp[0] < couplePos[1])] 
        maxVal = max(dataValsWithinRange)
        minVal = min(dataValsWithinRange)
        
        zeroVal = MeasurementAnalysisToolkit.getPointValueFromProfile(profileMeasuredData, 0)
        
        return (maxVal - minVal) / zeroVal
    
    def getProfileSymmetry(profileMeasuredData):
        '''Description: Get symmetry
            
            Arguments: Profile measured data
            
            Return: Symmetry or None if can't find couple positions.            
        '''
        couplePos = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData, 0.8)
        if len(couplePos) != 2:
            return None           
        
        dataPointsWithinRange = [dp for dp in profileMeasuredData.dataPoints if (dp[0] > couplePos[0] and dp[0] < couplePos[1])]        
        
        zeroVal = MeasurementAnalysisToolkit.getPointValueFromProfile(profileMeasuredData, 0)        
        
        flatMax = 0
        for i in range(len(dataPointsWithinRange)):
            dx = dataPointsWithinRange[i][1]
            dxs = MeasurementAnalysisToolkit.getPointValueFromProfile(profileMeasuredData, -dataPointsWithinRange[i][1])
            
            flat = abs(dx - dxs) / zeroVal
            if flatMax < flat:
                flatMax = flat
    
    def getProfilePenumbra(profileMeasuredData):
        '''Description: Get penumbra
            
            Arguments: Profile measured data
            
            Return: Penumbra or None if can't find couple positions.            
        '''
        couplePos20 = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData, 0.2)
        couplePos80 = MeasurementAnalysisToolkit.getValueCoordinates(profileMeasuredData, 0.8)
        if len(couplePos20) != 2 or len(couplePos80) != 2:
            return None

        penumbraLt = couplePos80[0] - couplePos20[0]
        penumbraRt = couplePos20[1] - couplePos80[1]       
        
        return [penumbraLt, penumbraRt]
        
    def getValueCoordinates(profileMeasuredData, coe = 0.5):
        dataPoints = profileMeasuredData.dataPoints
        
        doseVal = coe * max([dp[1] for dp in dataPoints])
        couplePos = []
        for i in range(len(dataPoints) - 2):
            former = dataPoints[i]
            later = dataPoints[i+1]
            
            product = (former[1] - doseVal) * (later[1] - doseVal)
            if(product < 0):
                couplePos.append((former[0] + later[0])/2)
            elif (product == 0):
                pos = (former[0] if former[1] == doseVal else later[0])
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
        
                    