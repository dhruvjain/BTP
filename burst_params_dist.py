import os
import fonte_nossdav_properties as p
import pickle
from collections import defaultdict
import operator

#####################################

def analyzeBurstParams (appName, traceName):
    
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
    p1 = []
    c1 = 0

    write2 = open(bp_burstduration,"w")
    p2 = []
    c2 = 0

    write3 = open(bp_iburstat,"w")
    p3 = []
    c3 = 0

    write4 = open(bp_avgpktsize,"w")
    p4 = []
    c4 = 0

    write5 = open(bp_avgpktiat,"w")
    p5 = []
    c5 = 0

    for burst in bursts:
        if (len(burst)<=20):
            bursts.remove(burst)

    prevBurstEndTime = 0
    c = 0
    for burst in bursts:
        #print(len(burst))
        burstSize = 0
        totalIAT = 0
        c = 0
        for packet in burst:
            if c>0:
                totalIAT += packet[1]
            burstSize += packet[3]
            c += 1

        pktCount = len(burst)
        #print("Packet Count: "+str(pktCount))
        avgPktSize = burstSize/pktCount
        if pktCount>1:
            avgIAT = totalIAT/(pktCount-1)
        else:
            avgIAT = 0
        burstDuration = burst[len(burst)-1][1] - burst[0][1]
        if (not (prevBurstEndTime==0)) and (burst[0][1] > prevBurstEndTime):
            burstIAT = burst[0][1] - prevBurstEndTime
        else:
            burstIAT = 0
        prevBurstEndTime = burst[0][1]

        if burstSize > 1:
            p1.append(burstSize)
        if burstDuration > 1:
            p2.append(burstDuration)
        if burstIAT > 1:
            p3.append(burstIAT)
        if avgPktSize > 1:
            p4.append(avgPktSize)
        if avgIAT > 1:
            p5.append(avgIAT)

        #writefp.write(str(c)+" "+str(burstSize)+" "+str(burstDuration)+" "+str(burstIAT)+" "+str(avgPktSize)+" "+str(avgIAT)+"\n")
        c += 1

    p1.sort() # Burst Size
    p2.sort() # Burst Duration
    p3.sort() # Burst IAT
    p4.sort() # Avg. Packet Size
    p5.sort() # Avg. IAT

    
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

    
    for i in range(0,len(p1)):
        write1.write(str(i)+" "+str(p1[i])+"\n")
    write1.close()

    for i in range(0,len(p2)):
        write2.write(str(i)+" "+str(p2[i])+"\n")
    write2.close()
    
    for i in range(0,len(p3)):
        write3.write(str(i)+" "+str(p3[i])+"\n")
    write3.close()

    for i in range(0,len(p4)):
        write4.write(str(i)+" "+str(p4[i])+"\n")
    write4.close()

    for i in range(0,len(p5)):
        write5.write(str(i)+" "+str(p5[i])+"\n")
    write5.close()
    

    cdf_bp_burstsize = os.path.join(burstParamsPlotPath,traceName+"_burstsize_cdf.plot")
    cdf_bp_burstduration = os.path.join(burstParamsPlotPath,traceName+"_burstduration_cdf.plot")
    cdf_bp_iburstat = os.path.join(burstParamsPlotPath,traceName+"_interburstarrivaltime_cdf.plot")
    cdf_bp_avgpktsize = os.path.join(burstParamsPlotPath,traceName+"_avgpktsize_cdf.plot")
    cdf_bp_avgpktiat = os.path.join(burstParamsPlotPath,traceName+"_avgpktiat_cdf.plot")

    fpw1 = open(cdf_bp_burstsize,'w')
    fpw2 = open(cdf_bp_burstduration, 'w')
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

