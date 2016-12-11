# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:51:26 2016

@author: cnshayit
"""

import re
import os
import numpy as np
import matplotlib.pyplot as plt
from measureddatasetprovider import MeasuredDataSetProvider
from measurementanalysistoolkit import MeasurementAnalysisToolkit as MAT

#from ptwdata import PtwData
#from ptwdatapoint import PtwDataPoint
from bdtdata16 import BdtData16

#bdt_path = 'linac.bdt'
#bdt_data = BdtData16(bdt_path)
#
#print(bdt_data.propertyDict['NOMINAL-ENERGY'])

#s = 'AB_06mv400.00x400.00.1015'
namepat = re.compile(r"(AB|GT|Z|DGBTA)(_)(\d+mv)(\d+.\d+x\d+.\d+)(.\d+)")
#properties = namepat.match(s).group(1, 2, 3, 4, 5)

#measured_data = MeasuredData('AB_06mv50.00x50.00.1015')

path = r'C:\Users\cnshayit\Desktop\innovation_python\!!!MC Data Library\Final.new.Validate\Measured'

measuredDataSetProvider = MeasuredDataSetProvider(path, namepat)
bResult = measuredDataSetProvider.getAllMeasuredDataInDir()
measuredDataSet = measuredDataSetProvider.measuredDataSet

Dper = MAT.extractPddPercentages(measuredDataSet[-1])



#plt.figure(figsize=(8,4))
#plt.plot(measuredDataSet[0].positions, measuredDataSet[0].measurements, 'b*')
##plt.plot(positions, measurements, 'r')
##plt.ylim(0, 15)
#plt.title('measurmed data')
#plt.legend()
#plt.show()



#path = 'testPtw.mcc'
#mccData = PtwData(path)
#
#count = len(mccData.scans)
#
#dataPoints = mccData.scans[0].datapoints;
#
#count2 = len(dataPoints)
#
#positions = [x.position for x in dataPoints]
#print(positions)
#measurements = [x.measurement for x in dataPoints]
#print(measurements)
#    
#plt.figure(figsize=(8,4))
#plt.plot(positions, measurements, 'b*')
#plt.plot(positions, measurements, 'r')
##plt.ylim(0, 15)
#plt.title('measurmed data')
#plt.legend()
#plt.show()