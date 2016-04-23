import os
import fonte_nossdav_properties as p
import pickle
import numpy as np
from collections import defaultdict
import operator

def getCDF(data, multiplier):

    dictBurstSize = defaultdict(int)

    for dp in data:
        granular_data = int(np.ceil(float(dp)*multiplier))
        dictBurstSize[dp] += 1

    totalFreq = len(data)
    absBurstSize = sorted(dictBurstSize.items(), key=operator.itemgetter(0,1))
    cdfBurstSize = []

    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absBurstSize:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfBurstSize.append((dataPoint[0],cdf))

    return cdfBurstSize

#####################################

def writeIntoFile(traceName, data, filename):

    burstParamsPlotPath = os.path.join(p.BURSTS_PLOT_PATH,traceName)
    if not os.path.exists(burstParamsPlotPath):
        os.makedirs(burstParamsPlotPath)

    #Unsorted
    path = os.path.join(burstParamsPlotPath,traceName+"_unsorted-"+filename+".plot")
    writep = open(path,"w")
    for i in range(0, len(data)):
        writep.write(str(i)+" "+str(data[i])+"\n")
    writep.close()

    #Cdf
    path = os.path.join(burstParamsPlotPath,traceName+"_cdf-"+filename+".plot")
    writep = open(path,"w")

    cdfBurstSize = getCDF(data, p.multiplier)
    
    for i in range(0, len(cdfBurstSize)):
        writep.write(str(cdfBurstSize[i][0]) + " " + str(cdfBurstSize[i][1]) + "\n")
    writep.close()

    #Sorted
    data.sort()
    path = os.path.join(burstParamsPlotPath,traceName+"_sorted-"+filename+".plot")
    writep = open(path,"w")
    for i in range(0,len(data)):
        writep.write(str(i)+" "+str(data[i])+"\n")
    writep.close()


#####################################

def analyzeBurstParams (appName, traceName):
    
    p1 = []  
    p2 = []  
    p3 = []  
    p4 = []  
    p5 = []  
    p6 = []  
    p7 = [0]
    p8 = []
    
    burstPath = os.path.join(p.BURSTS_PARENT_PATH,appName,traceName+".burst")
    bursts = pickle.load(open(burstPath,"rb"))

    print traceName
    prevBurstEndTime = 0
    total_Data = 0
    for i, burst in enumerate(bursts):
        burstSize = 0
        totalIAT = 0

        for index, packet in enumerate(burst[1:]):
            
            pktiat = (burst[index+1][1] - burst[index][1])*p.multiplier
            if pktiat<1000:
                p6.append(pktiat)
            else:
                p8.append(pktiat)

            totalIAT += burst[index+1][1] - burst[index][1]
            burstSize += packet[3]

        pktCount = len(burst)
        if pktCount==1:
            print "pkt count = 0 of ", i

            for packet in burst:
                print packet

        avgIAT = totalIAT*p.multiplier*1.0/(pktCount-1)
        avgPktSize = burstSize*1.0/pktCount
        burstDuration = burst[len(burst)-1][1] - burst[0][1]
        
        if (prevBurstEndTime!=0):
            burstIAT = burst[0][1] - prevBurstEndTime
            if burstIAT >= 50:
                total_Data = 0
                '''
                print "\n\nburstSize = ", burstSize
                print "burstDuration = ", burstDuration
                print "avgIAT = ", avgIAT
                '''
            else:
                p3.append(burstIAT)
        else:
            burstIAT = 0

        total_Data += burstSize/1000
        prevBurstEndTime = burst[len(burst)-1][1]
        burstSize = burstSize*1.0/1000

        p1.append(burstSize)
        p2.append(burstDuration)
        p4.append(avgPktSize)
        p5.append(avgIAT)
        p7.append(total_Data)

    
    writeIntoFile(traceName, p1, "burstsize")
    writeIntoFile(traceName, p2, "burstduration")
    writeIntoFile(traceName, p3, "interburstarrivaltime")
    writeIntoFile(traceName, p4, "avgpktsize")
    writeIntoFile(traceName, p5, "avgpktiat")
    writeIntoFile(traceName, p6, "pktiatless")
    writeIntoFile(traceName, p7, "bufferstatus")
    writeIntoFile(traceName, p8, "pktiatmore")

    print "done"

    return

#####################################

def main():
    
    appNames = ['YouTube']

    for app in appNames:
        if os.path.exists(os.path.join(p.BURSTS_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.BURSTS_PARENT_PATH,app)):
                if not filePath.startswith('.'):
                    traceName = filePath.split('.')[0]
                    analyzeBurstParams(app,traceName)
    return

#####################################

if __name__ == "__main__":
    main()

