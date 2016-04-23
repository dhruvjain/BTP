import os
import fonte_nossdav_properties as p
import pickle
from collections import defaultdict
import operator

#####################################

def writeIntoFile(tracename, data, filename):

    burstParamsPlotPath = os.path.join(p.BURSTS_PLOT_PATH,traceName)
    if not os.path.exists(burstParamsPlotPath):
        os.makedirs(burstParamsPlotPath)

    #Unsorted
    path = os.path.join(burstParamsPlotPath,traceName+"unsorted_"+filename+".plot")
    writep = open(path,"w")
    for i in range(0,len(data)):
        writep.write(str(i)+" "+str(data[i])+"\n")
    writep.close()

    #Cdf
    path = os.path.join(burstParamsPlotPath,traceName+"_"+filename+"-cdf.plot")
    writep = open(path,"w")

    dictBurstSize = defaultdict(int)
    for dp in data:
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

    for i in range(0, len(cdfBurstSize)):
        writep.write(str(i) + " " + str(cdfBurstSize[i][0]) + " " + str(cdfBurstSize[i][1]) + "\n")
    writep.close()
    

    #Sorted
    data.sort()
    path = os.path.join(burstParamsPlotPath,traceName+"sorted_"+filename+".plot")
    writep = open(path,"w")
    for i in range(0,len(data)):
        writep.write(str(i)+" "+str(data[i])+"\n")
    writep.close()

#####################################

def getcdf():


   

   

    cdf_bp_burstsize = os.path.join(burstParamsPlotPath,traceName+"_burstsize_cdf.plot")
    fpw = open(cdf_bp_avgpktiat, 'w')

    for i in range(0,len(cdfBurstSize)):
        fpw1.write(str(i) + " " + str(cdfBurstSize[i][0]) + " " + str(cdfBurstSize[i][1]) + "\n")
    fpw1.close()


def analyzeBurstParams (appName, traceName):
    
    p1 = []  #Bytes vs burst
    p2 = []  #sec vs burst
    p3 = []  #sec vs burst
    p4 = []  #avg packet size (Bytes) vs burst
    p5 = []  #microsecond vs bursts
    p6 = []  #us vs pkt no.
    p7 = [0]
    p8 = []
    
    burstPath = os.path.join(p.BURSTS_PARENT_PATH,appName,traceName+".burst")
    bursts = pickle.load(open(burstPath,"rb"))
    

    bp_burstsize = 
    bp_burstduration = os.path.join(burstParamsPlotPath,traceName+"_burstduration.plot")
    bp_iburstat = os.path.join(burstParamsPlotPath,traceName+"_interburstarrivaltime.plot")
    bp_avgpktsize = os.path.join(burstParamsPlotPath,traceName+"_avgpktsize.plot")
    bp_avgpktiat = os.path.join(burstParamsPlotPath,traceName+"_avgpktiat.plot")
    bp_pktiat = os.path.join(burstParamsPlotPath,traceName+"_pktiatless.plot")
    bp_totsize = os.path.join(burstParamsPlotPath,traceName+"_bufferstatus.plot")
    bp_pktiat_more = os.path.join(burstParamsPlotPath,traceName+"_pktiatmore.plot")

    write1 = open(bp_burstsize,"w")
    write2 = open(bp_burstduration,"w")
    write3 = open(bp_iburstat,"w")
    write4 = open(bp_avgpktsize,"w")
    write5 = open(bp_avgpktiat,"w")
    write6 = open(bp_pktiat,"w")
    write7 = open(bp_totsize, "w")
    write8 = open(bp_pktiat_more,"w")

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

        avgpktiat = totalIAT*p.multiplier*1.0/(pktCount-1)
        avgPktSize = burstSize*1.0/pktCount
        burstDuration = burst[len(burst)-1][1] - burst[0][1]
        
        if (prevBurstEndTime!=0):
            burstIAT = burst[0][1] - prevBurstEndTime
            if burstIAT >= 50:
                total_Data = 0
                '''
                print "\n\nburstSize = ", burstSize
                print "burstDuration = ", burstDuration
                print "avgpktiat = ", avgpktiat
                '''
            else:
                p3.append(burstIAT)
        else:
            burstIAT = 0

        total_Data += burstSize/1000
        prevBurstEndTime = burst[len(burst)-1][1]

        burstSize = burstSize*1.0/1000
        burstSize = burstSize/1000
        p1.append(burstSize)
        p2.append(burstDuration)
        p4.append(avgPktSize)
        p5.append(avgpktiat)
        p7.append(total_Data)

    #print p1
    p1.sort() # Burst Size
    p2.sort() # Burst Duration
    p3.sort() # Burst IAT
    p4.sort() # Avg. Packet Size
    p5.sort() # Avg. IAT
    p6.sort() # IAT
    p8.sort()

    writeIntoFile(tracename, p1, "burstsize")
    writeIntoFile(tracename, p2, "burstduration")
    writeIntoFile(tracename, p3, "interburstarrivaltime")
    writeIntoFile(tracename, p4, "avgpktsize")
    writeIntoFile(tracename, p5, "avgpktiat")
    writeIntoFile(tracename, p6, "pktiatless")
    writeIntoFile(tracename, p7, "bufferstatus")
    writeIntoFile(tracename, p8, "pktiatmore")
   

    cdf_bp_burstsize = os.path.join(burstParamsPlotPath,traceName+"_burstsize_cdf.plot")
    cdf_bp_burstduration = os.path.join(burstParamsPlotPath,traceName+"_burstduration_cdf.plot")
    cdf_bp_iburstat = os.path.join(burstParamsPlotPath,traceName+"_interburstarrivaltime_cdf.plot")
    cdf_bp_avgpktsize = os.path.join(burstParamsPlotPath,traceName+"_avgpktsize_cdf.plot")
    cdf_bp_avgpktiat = os.path.join(burstParamsPlotPath,traceName+"_avgpktiat_cdf.plot")

    print "done"

   


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

    '''
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

