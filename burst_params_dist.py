import os
import fonte_nossdav_properties as p
import pickle
from collections import defaultdict
import operator

#####################################

def writeIntoFile(fileptr, data):
    for i in range(0,len(data)):
        fileptr.write(str(i)+" "+str(data[i])+"\n")
    fileptr.close()

#####################################

def analyzeBurstParams (appName, traceName):
    
    p1 = p2 = p3 = p4 = p5 = []
    
    burstPath = os.path.join(p.BURSTS_PARENT_PATH,appName,traceName+".burst")
    bursts = pickle.load(open(burstPath,"rb"))
    burstParamsPlotPath = os.path.join(p.BURSTS_PLOT_PATH,traceName)
    if not os.path.exists(burstParamsPlotPath):
        os.makedirs(burstParamsPlotPath)

    bp_burstsize = os.path.join(burstParamsPlotPath,traceName+"_burstsize.plot")
    bp_burstduration = os.path.join(burstParamsPlotPath,traceName+"_burstduration.plot")
    bp_iburstat = os.path.join(burstParamsPlotPath,traceName+"_interburstarrivaltime.plot")
    bp_avgpktsize = os.path.join(burstParamsPlotPath,traceName+"_avgpktsize.plot")
    bp_avgpktiat = os.path.join(burstParamsPlotPath,traceName+"_avgpktiat.plot")

    write1 = open(bp_burstsize,"w")
    write2 = open(bp_burstduration,"w")
    write3 = open(bp_iburstat,"w")
    write4 = open(bp_avgpktsize,"w")
    write5 = open(bp_avgpktiat,"w")
    
    prevBurstEndTime = 0
    for burst in bursts:
        burstSize = 0
        totalIAT = 0

        for index, packet in enumerate(burst[1:]):
            totalIAT += burst[index+1][1] - burst[index][1]
            burstSize += packet[3]

        pktCount = len(burst)
        avgPktSize = burstSize/pktCount
        avgIAT = totalIAT/(pktCount-1)
        burstDuration = burst[len(burst)-1][1] - burst[0][1]

        if (burst[0][1] > prevBurstEndTime):
            burstIAT = burst[0][1] - prevBurstEndTime

        prevBurstEndTime = burst[len(burst)-1][1]

        p1.append(burstSize)
        p2.append(burstDuration)
        p3.append(burstIAT)
        p4.append(avgPktSize)
        p5.append(avgIAT)

    p1.sort() # Burst Size
    p2.sort() # Burst Duration
    p3.sort() # Burst IAT
    p4.sort() # Avg. Packet Size
    p5.sort() # Avg. IAT
    
    writeIntoFile(write1, p1)
    writeIntoFile(write2, p2)
    writeIntoFile(write3, p3)
    writeIntoFile(write4, p4)
    writeIntoFile(write5, p5)

    '''
    dictBurstSize = defaultdict(int)
    for dp in p1:
        dictBurstSize[dp] += 1
    totalFreq = len(p1)
    absBurstSize = sorted(dictBurstSize.items(), key=operator.itemgetter(0,1))
    cdfBurstSize = []

    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absBurstSize:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfBurstSize.append((dataPoint[0],cdf))


    dictBurstDuration = defaultdict(int)
    for dp in p2:
        dictBurstDuration[dp] += 1
    totalFreq = len(p2)
    absBurstDuration = sorted(dictBurstDuration.items(), key=operator.itemgetter(0,1))
    cdfBurstDuration = []
   
    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absBurstDuration:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfBurstDuration.append((dataPoint[0],cdf))


    dictBurstIAT = defaultdict(int)
    for dp in p3:
        dictBurstIAT[dp] += 1
    totalFreq = len(p3)
    absBurstIAT = sorted(dictBurstIAT.items(), key=operator.itemgetter(0,1))
    cdfBurstIAT = []
    
    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absBurstIAT:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfBurstIAT.append((dataPoint[0],cdf))

    
    dictAvgPacketSize = defaultdict(int)
    for dp in p4:
        dictAvgPacketSize[dp] += 1
    totalFreq = len(p4)
    absAvgPacketSize = sorted(dictAvgPacketSize.items(), key=operator.itemgetter(0,1))
    cdfAvgPacketSize = []
    
    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absAvgPacketSize:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfAvgPacketSize.append((dataPoint[0],cdf))

    
    dictAvgIAT = defaultdict(int)
    for dp in p5:
        dictAvgIAT[dp] += 1
    totalFreq = len(p5)
    absAvgIAT = sorted(dictAvgIAT.items(), key=operator.itemgetter(0,1))
    cdfAvgIAT = []
    
    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in absAvgIAT:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        cdfAvgIAT.append((dataPoint[0],cdf))

    
    
    

    cdf_bp_burstsize = os.path.join(burstParamsPlotPath,traceName+"_burstsize_cdf.plot")
    cdf_bp_burstduration = os.path.join(burstParamsPlotPath,traceName+"_burstduration_cdf.plot")
    cdf_bp_iburstat = os.path.join(burstParamsPlotPath,traceName+"_interburstarrivaltime_cdf.plot")
    cdf_bp_avgpktsize = os.path.join(burstParamsPlotPath,traceName+"_avgpktsize_cdf.plot")
    cdf_bp_avgpktiat = os.path.join(burstParamsPlotPath,traceName+"_avgpktiat_cdf.plot")

    fpw1 = open(cdf_bp_burstsize,'w')
    #fpw2 = open(cdf_bp_burstduration, 'w')
    fpw3 = open(cdf_bp_iburstat, 'w')
    fpw4 = open(cdf_bp_avgpktsize, 'w')
    fpw5 = open(cdf_bp_avgpktiat, 'w')

    for i in range(0,len(cdfBurstSize)):
        fpw1.write(str(i) + " " + str(cdfBurstSize[i][0]) + " " + str(cdfBurstSize[i][1]) + "\n")
    fpw1.close()
    
    for i in range(0,len(cdfBurstDuration)):
        fpw2.write(str(i) + " " + str(cdfBurstDuration[i][0]) + " " + str(cdfBurstDuration[i][1]) + "\n")
    fpw2.close()
    
    for i in range(0,len(cdfBurstIAT)):
        fpw3.write(str(i) + " " + str(cdfBurstIAT[i][0]) + " " + str(cdfBurstIAT[i][1]) + "\n")
    fpw3.close()

    for i in range(0,len(cdfAvgPacketSize)):
        fpw4.write(str(i) + " " + str(cdfAvgPacketSize[i][0]) + " " + str(cdfAvgPacketSize[i][1]) + "\n")
    fpw4.close()

    for i in range(0,len(cdfAvgIAT)):
        fpw5.write(str(i) + " " + str(cdfAvgIAT[i][0]) + " " + str(cdfAvgIAT[i][1]) + "\n")
    fpw5.close()
    '''
    return

#####################################

def main():
    
    appNames = ['YouTube']

    for app in appNames:
        if os.path.exists(os.path.join(p.CSV_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.CSV_PARENT_PATH,app)):
                if not filePath.startswith('.'):
                    traceName = filePath.split('.')[0]
                    analyzeBurstParams(app,traceName)

    return

#####################################

if __name__ == "__main__":
    main()

